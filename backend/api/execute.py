from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uuid

from backend.services.code_executor import CodeExecutor
from backend.models.schema import Problem, Submission, User
from backend.database import get_db

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
    results: List[TestResult]

@router.post("/execute", response_model=ExecuteResponse)

async def execute_code(req: ExecuteRequest, db: Session = Depends(get_db)):
    """
    Execute user code against problem's test cases.
    Stores submission and returns results.
    """
    # 1. Fetch the problem from database
    problem = db.query(Problem).filter(Problem.id == req.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # 2. Fetch the user 
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Execute the code against test cases
    executor = CodeExecutor()
    result = executor.execute(req.code, problem.test_cases)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # 4. Store the submission in database
    submission = Submission(
        id=str(uuid.uuid4()),
        user_id=req.user_id,
        problem_id=req.problem_id,
        code=req.code,
        passed=result["passed"],
        passed_count=result["passed_count"],
        total_count=result["total_count"]
    )
    db.add(submission)
    db.commit()

    # 5. Return the results
    return ExecuteResponse(
        passed=result["passed"],
        passed_count=result["passed_count"],
        total_count=result["total_count"],
        results=result["results"]
    )