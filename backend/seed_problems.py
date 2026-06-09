import uuid
from database import SessionLocal
from models.schema import Problem

def seed_problems():
    db = SessionLocal()
    
    # Check if problems already exist
    if db.query(Problem).count() > 0:
        print("Problems already seeded. Skipping.")
        db.close()
        return
    
    problem = Problem(
        id="prob_easy_1",
        title="Add Two Numbers",
        description="Write a function that takes two numbers and returns their sum.",
        difficulty="easy",
        topic="basics",
        starter_code="def add(a, b):\n    # Your code here\n    pass\n\nprint(add(int(input()), int(input())))",
        test_cases=[
            {"input": "2\n3", "expected_output": "5"},
            {"input": "10\n20", "expected_output": "30"}
        ]
    )
    
    db.add(problem)
    db.commit()
    print(f"Added problem: {problem.title}")
    db.close()

if __name__ == "__main__":
    seed_problems()