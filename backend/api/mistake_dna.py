from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.schema import MistakeProfile, User

router = APIRouter(prefix="/api/mistake-dna", tags=["mistake-dna"])

@router.get("/user/{user_id}")
def get_mistake_dna(user_id: str, db: Session = Depends(get_db)):
    """Return user's mistake DNA profile: mastery, mistake counts, recommendation."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.query(MistakeProfile).filter(MistakeProfile.user_id == user_id).first()
    if not profile:
        return {
            "mastery": {},
            "mistakes": {},
            "recommendation": "Start solving problems to build your Mistake DNA."
        }

    # Collect mastery scores (0-100)
    mastery = {
        "loops": profile.loops_mastery,
        "functions": profile.functions_mastery,
        "recursion": profile.recursion_mastery,
        "arrays": profile.arrays_mastery,
        "dicts": profile.dicts_mastery
    }

    # Collect mistake counts
    mistakes = {
        "syntax_errors": profile.syntax_errors,
        "index_errors": profile.index_errors,
        "logic_errors": profile.logic_errors,
        "recursion_errors": profile.recursion_errors
    }

    # Generate recommendation based on weakest area
    weakest_topic = min(mastery, key=lambda t: mastery.get(t, 0))
    weakest_score = mastery.get(weakest_topic, 0)
    recommendation = f"You're weakest at **{weakest_topic}** ({weakest_score}%). Practice more in this area."

    return {
        "mastery": mastery,
        "mistakes": mistakes,
        "recommendation": recommendation
    }