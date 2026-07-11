from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.schema import Problem
from services.problem_recommender import ProblemRecommender

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
            "topic": p.topic,
        }
        for p in problems
    ]


@router.get("/recommended/{user_id}")
async def get_recommended_problem(user_id: str, db: Session = Depends(get_db)):
    """Get a recommended problem for the user."""
    problem = ProblemRecommender.get_recommendation(db, user_id)

    if not problem:
        raise HTTPException(status_code=404, detail="No problems available")

    return {
        "id": problem.id,
        "title": problem.title,
        "description": problem.description,
        "difficulty": problem.difficulty,
        "topic": problem.topic,
        "starter_code": problem.starter_code,
    }


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
        "test_cases": problem.test_cases,
    }
