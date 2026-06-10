from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models.schema import Problem
from backend.database import get_db

router = APIRouter(prefix="/api/problems", tags=["problems"])

@router.get("/")
def get_all_problems(db: Session = Depends(get_db)):
    """Return list of all problems (id, title, difficulty, topic)."""
    problems = db.query(Problem).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "difficulty": p.difficulty,
            "topic": p.topic
        }
        for p in problems
    ]

@router.get("/{problem_id}")
def get_problem(problem_id: str, db: Session = Depends(get_db)):
    """Return full problem details (including description, starter_code, test_cases)."""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return {
        "id": problem.id,
        "title": problem.title,
        "description": problem.description,
        "difficulty": problem.difficulty,
        "topic": problem.topic,
        "starter_code": problem.starter_code,
        "test_cases": problem.test_cases
    }