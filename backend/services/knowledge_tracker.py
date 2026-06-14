from sqlalchemy.orm import Session
from backend.models.schema import MistakeProfile, Problem, Submission

class KnowledgeTracker:
    """Update student's knowledge/mistake profile after each submission."""

    @staticmethod
    def update_profile(db: Session, user_id: str, submission: Submission, mistake_types: list):
        """
        Update MistakeProfile based on submission:
        - If passed: +10 mastery for that topic (max 100)
        - If failed: -5 mastery (min 0), +1 to relevant mistake counters
        """
        # Get the problem to know the topic
        problem = db.query(Problem).filter(Problem.id == submission.problem_id).first()
        if not problem:
            return

        # Get or create profile
        profile = db.query(MistakeProfile).filter(MistakeProfile.user_id == user_id).first()
        if not profile:
            profile = MistakeProfile(user_id=user_id)
            db.add(profile)
            db.commit()  # save to get ID

        # Map topic to attribute name
        topic_field = f"{problem.topic}_mastery"
        current_mastery = getattr(profile, topic_field, 0)

        if submission.passed:
            # Increase mastery (max 100)
            new_mastery = min(100, current_mastery + 10)
        else:
            # Decrease mastery (min 0)
            new_mastery = max(0, current_mastery - 5)

        setattr(profile, topic_field, new_mastery)

        # Update mistake counters
        for mistake in mistake_types:
            mistake_field = f"{mistake}_errors"  # e.g., syntax_errors
            if hasattr(profile, mistake_field):
                current_count = getattr(profile, mistake_field, 0)
                setattr(profile, mistake_field, current_count + 1)

        db.commit()
        return profile