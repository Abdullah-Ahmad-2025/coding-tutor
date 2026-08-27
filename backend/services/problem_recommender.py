from sqlalchemy.orm import Session
from backend.models.schema import MistakeProfile, Problem, Submission

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

        # ============================================================
        # FIX: Only consider topics the user has actually attempted
        # ============================================================

        # 1. Get all topics the user has attempted (via submissions)
        attempted_topics = (
            db.query(Problem.topic)
            .join(Submission, Submission.problem_id == Problem.id)
            .filter(Submission.user_id == user_id)
            .distinct()
            .all()
        )
        attempted_topic_names = [t[0] for t in attempted_topics]

        # 2. If user hasn't attempted any problem yet, return an easy problem
        if not attempted_topic_names:
            problem = db.query(Problem).filter(Problem.difficulty == "easy").first()
            return problem

        # 3. Build mastery dictionary
        mastery_map = {
            "basics": profile.basics_mastery,
            "loops": profile.loops_mastery,
            "functions": profile.functions_mastery,
            "recursion": profile.recursion_mastery,
            "arrays": profile.arrays_mastery,
            "dicts": profile.dicts_mastery,
            "strings": profile.strings_mastery
        }

        # 4. Filter only topics the user has actually attempted
        filtered_topics = [
            (topic, mastery_map[topic])
            for topic in attempted_topic_names
            if topic in mastery_map
        ]

        # 5. If for some reason no topics remain (should not happen), fallback
        if not filtered_topics:
            filtered_topics = list(mastery_map.items())

        # 6. Find the weakest topic among those attempted
        weakest_topic, weakest_score = min(filtered_topics, key=lambda x: x[1])

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

        # Last resort: any easy problem (even if already solved)
        if not problem:
            problem = db.query(Problem).filter(Problem.difficulty == "easy").first()

        return problem