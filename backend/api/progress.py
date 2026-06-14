from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.schema import User, Submission, Problem

router = APIRouter(prefix="/api/progress", tags=["progress"])

@router.get("/user/{user_id}")
def get_user_progress(user_id: str, db: Session = Depends(get_db)):
    """
    Return progress for a user:
    - problems_solved: count of distinct problems fully passed
    - total_attempts: total submissions
    - topics: dict of topic -> {attempts, solved, mastery}
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all submissions for this user
    submissions = db.query(Submission).filter(Submission.user_id == user_id).all()

    if not submissions:
        return {
            "problems_solved": 0,
            "total_attempts": 0,
            "topics": {}
        }

    # Count distinct problems fully passed
    solved_problem_ids = set()
    for sub in submissions:
        if sub.passed:  # all tests passed
            solved_problem_ids.add(sub.problem_id)
    problems_solved = len(solved_problem_ids)

    total_attempts = len(submissions)

    # Build topic stats
    topic_stats = {}

    for sub in submissions:
        # Get problem details
        problem = db.query(Problem).filter(Problem.id == sub.problem_id).first()
        if not problem:
            continue
        topic = problem.topic
        if topic not in topic_stats:
            topic_stats[topic] = {"attempts": 0, "solved": 0}
        topic_stats[topic]["attempts"] += 1
        if sub.passed:
            topic_stats[topic]["solved"] += 1

    # Convert to mastery percentages
    topics_result = {}
    for topic, stats in topic_stats.items():
        mastery = int((stats["solved"] / stats["attempts"]) * 100) if stats["attempts"] > 0 else 0
        topics_result[topic] = {
            "attempts": stats["attempts"],
            "solved": stats["solved"],
            "mastery": mastery
        }

    return {
        "problems_solved": problems_solved,
        "total_attempts": total_attempts,
        "topics": topics_result
    }