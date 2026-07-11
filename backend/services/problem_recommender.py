from sqlalchemy.orm import Session
from models.schema import MistakeProfile, Problem, Submission

class ProblemRecommender:
    """Recommend next problem based on student's weaknesses."""

    @staticmethod
    def get_recommendation(db: Session, user_id: str):
        """
        Find weakest topic, recommend a problem in that topic with appropriate difficulty.
        """
        # Get user's profile
        profile = db.query(MistakeProfile).filter(MistakeProfile.user_id == user_id).first()

        if not profile:
            # No history → start with an easy problem
            problem = db.query(Problem).filter(Problem.difficulty == "easy").first()
            return problem

        # Find weakest topic (lowest mastery)
        topics = [
            ("basics", profile.basics_mastery),
            ("loops", profile.loops_mastery),
            ("functions", profile.functions_mastery),
            ("recursion", profile.recursion_mastery),
            ("arrays", profile.arrays_mastery),
            ("dicts", profile.dicts_mastery),
            ("strings", profile.strings_mastery)
        ]
        weakest_topic, weakest_score = min(topics, key=lambda x: x[1])

        # Determine difficulty based on mastery
        if weakest_score > 70:
            difficulty = "hard"
        elif weakest_score > 40:
            difficulty = "medium"
        else:
            difficulty = "easy"

        # Get solved problem IDs (passed submissions)
        solved_ids = db.query(Submission.problem_id).filter(
            Submission.user_id == user_id,
            Submission.passed == True
        ).all()
        solved_ids = [s[0] for s in solved_ids]

        def unsolved_filter(query):
            if solved_ids:
                return query.filter(~Problem.id.in_(solved_ids))
            return query

        # Find a problem in that topic + difficulty, not solved yet
        problem = unsolved_filter(
            db.query(Problem).filter(
                Problem.topic == weakest_topic,
                Problem.difficulty == difficulty,
            )
        ).first()

        # Fallback: if no such problem, get any problem of that difficulty not solved
        if not problem:
            problem = unsolved_filter(
                db.query(Problem).filter(Problem.difficulty == difficulty)
            ).first()

        # Final fallback: any easy problem not yet solved
        if not problem:
            problem = unsolved_filter(
                db.query(Problem).filter(Problem.difficulty == "easy")
            ).first()

        # Last resort: any easy problem
        if not problem:
            problem = db.query(Problem).filter(Problem.difficulty == "easy").first()

        return problem