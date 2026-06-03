import sys
import os

# Add parent directory to path so we can import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.code_executor import CodeExecutor

def test_executor():
    executor = CodeExecutor()

    # Simple test: add two numbers
    code = """
def add(a, b):
    return a + b

print(add(int(input()), int(input())))
"""

    test_cases = [
        {"input": "2\n3", "expected_output": "5"},
        {"input": "10\n20", "expected_output": "30"}
    ]

    print("=" * 50)
    print("Piston API Test Results")
    print("=" * 50)

    result = executor.execute(code, test_cases)

    for r in result["results"]:
        status = "✓" if r["passed"] else "✗"
        print(f"\n{status} Input: {r['input']}")
        print(f"  Expected: {r['expected']}")
        print(f"  Got: {r['actual']}")
        print(f"  Status: {r['status']}")

    print(f"\n{result['passed_count']}/{result['total_count']} tests passed")
    print(f"All passed: {result['passed']}")

if __name__ == "__main__":
    test_executor()