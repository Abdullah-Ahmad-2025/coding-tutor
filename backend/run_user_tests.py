import sys
import os
import asyncio
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.api.execute import execute_code, ExecuteRequest

async def main():
    db = SessionLocal()
    user_id = "1fdc2d9c-07f2-4627-b2b6-20808a438380"
    
    print("=" * 70)
    print("RUNNING USER TEST SCENARIOS")
    print("=" * 70)
    
    # Scenario 1: Syntax error (missing colon)
    print("\n[SCENARIO 1] Submitting Syntax Error code: 'def add(a, b) return a+b'")
    req1 = ExecuteRequest(
        code="""
def add(a, b)
    return a + b
print(add(int(input()), int(input())))
""",
        problem_id="prob_easy_1",
        user_id=user_id
    )
    res1 = await execute_code(req1, db)
    print("API Response:")
    print(json.dumps(res1.model_dump(), indent=2))
    
    # Scenario 2: Logic error (subtraction instead of addition)
    print("\n[SCENARIO 2] Submitting Logic Error code: 'def add(a,b): return a-b'")
    req2 = ExecuteRequest(
        code="""
def add(a, b):
    return a - b
print(add(int(input()), int(input())))
""",
        problem_id="prob_easy_1",
        user_id=user_id
    )
    res2 = await execute_code(req2, db)
    print("API Response:")
    print(json.dumps(res2.model_dump(), indent=2))
    
    # Scenario 3: Index error (out of range index access on Find Maximum in List)
    print("\n[SCENARIO 3] Submitting Index Error code: accessing out-of-range index")
    req3 = ExecuteRequest(
        code="""
def find_max(lst):
    # accessing index 10 on a list of length 5 (out of range index)
    return lst[10]

lst = list(map(int, input().split()))
print(find_max(lst))
""",
        problem_id="prob_medium_1",
        user_id=user_id
    )
    res3 = await execute_code(req3, db)
    print("API Response:")
    print(json.dumps(res3.model_dump(), indent=2))
    
    db.close()

if __name__ == "__main__":
    asyncio.run(main())
