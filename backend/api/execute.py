from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from services.code_executor import CodeExecutor
from services.mistake_detector import MistakeDetector
from services.knowledge_tracker import KnowledgeTracker
from models.schema import Problem, Submission, User
from database import get_db

router = APIRouter(prefix="/api", tags=["execute"])

class ExecuteRequest(BaseModel):
    code: str
    problem_id: str
    user_id: str

class TestResult(BaseModel):
    input: str
    expected: str
    actual: str
    passed: bool
    status: str

class ExecuteResponse(BaseModel):
    passed: bool
    passed_count: int
    total_count: int
    results: list
    mistakes: list = []
    primary_mistake: str = ""
    mistake_details: list = []

@router.post("/execute", response_model=ExecuteResponse)
async def execute_code(req: ExecuteRequest, db: Session = Depends(get_db)):
    # Fetch problem and user
    problem = db.query(Problem).filter(Problem.id == req.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        # Auto-create user for development (optional)
        user = User(id=req.user_id, email=f"{req.user_id}@temp.com", name="Auto User", password_hash="dummy")
        db.add(user)
        db.commit()

    # Reject empty submissions
    if not req.code or not req.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty. Please write your solution before submitting.")

    # Execute code
    executor = CodeExecutor()
    result = executor.execute(req.code, problem.test_cases)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Detect mistakes
    mistake_result = MistakeDetector.analyze_code(req.code, result)
    mistake_types = mistake_result["mistakes"]
    primary_mistake = mistake_result.get("primary_mistake", "")
    
    # Format detailed mistake messages
    mistake_details = [
        {"type": m, "message": MistakeDetector.get_mistake_message(m)}
        for m in mistake_types
    ]

    # Store submission
    submission = Submission(
        id=str(uuid.uuid4()),
        user_id=req.user_id,
        problem_id=req.problem_id,
        code=req.code,
        passed=result["passed"],
        passed_count=result["passed_count"],
        total_count=result["total_count"],
        mistakes=mistake_types
    )
    db.add(submission)
    db.commit()

    # Update knowledge profile
    KnowledgeTracker.update_profile(db, req.user_id, submission, mistake_types)

    return ExecuteResponse(
        passed=result["passed"],
        passed_count=result["passed_count"],
        total_count=result["total_count"],
        results=result["results"],
        mistakes=mistake_types,
        primary_mistake=primary_mistake,
        mistake_details=mistake_details
    )