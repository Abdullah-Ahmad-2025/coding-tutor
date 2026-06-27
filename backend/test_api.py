import sys
import os
import asyncio

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.init_db import init_db
from backend.seed_problems import seed_problems
from backend.api.execute import execute_code, ExecuteRequest
from backend.models.schema import User, MistakeProfile

async def run_integration_test():
    print("=" * 60)
    print("Running Integration Test for database & execute API")
    print("=" * 60)
    
    # 1. Initialize and seed DB
    init_db()
    seed_problems()
    
    db = SessionLocal()
    
    # Ensure test user exists or gets created
    user_id = "1fdc2d9c-07f2-4627-b2b6-20808a438380"
    
    # 2. Make an API call mock to execute_code with shadowing builtin mistake
    req = ExecuteRequest(
        code="""
def add(a, b):
    sum = a + b
    return sum
print(add(int(input()), int(input())))
""",
        problem_id="prob_easy_1",
        user_id=user_id
    )
    
    print("Calling execute_code API handler...")
    response = await execute_code(req, db)
    
    print("\nAPI Response:")
    print(f"  Passed: {response.passed}")
    print(f"  Passed Count: {response.passed_count}/{response.total_count}")
    print(f"  Mistakes detected: {response.mistakes}")
    print(f"  Primary mistake: {response.primary_mistake}")
    print(f"  Mistake details: {response.mistake_details}")
    
    # Assertions
    assert response.passed == True
    assert "shadowing_builtin" in response.mistakes
    assert response.primary_mistake == "shadowing_builtin"
    
    # Check if MistakeProfile was created in DB and has generated a primary key ID!
    profile = db.query(MistakeProfile).filter(MistakeProfile.user_id == user_id).first()
    assert profile is not None
    assert profile.id is not None
    assert len(profile.id) > 0
    print(f"\n[SUCCESS] MistakeProfile successfully created with generated ID: {profile.id}")
    print(f"  Basics Mastery: {profile.basics_mastery}%")
    assert profile.basics_mastery == 10
    print(f"  Syntax Errors Count: {profile.syntax_errors}")
    print(f"  Index Errors Count: {profile.index_errors}")
    print(f"  Recursion Errors Count: {profile.recursion_errors}")
    
    db.close()
    print("\nALL INTEGRATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_integration_test())
