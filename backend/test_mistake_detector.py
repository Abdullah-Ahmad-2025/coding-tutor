import sys
import os

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.code_executor import CodeExecutor
from backend.services.mistake_detector import MistakeDetector

def run_test_case(name: str, code: str, test_cases: list, expected_mistake: str):
    executor = CodeExecutor()
    execution_result = executor.execute(code, test_cases)
    
    # Run analysis
    analysis = MistakeDetector.analyze_code(code, execution_result)
    mistakes = analysis["mistakes"]
    primary = analysis["primary_mistake"]
    
    passed = expected_mistake in mistakes
    status = "PASS" if passed else "FAIL"
    
    print(f"[{status}] Test: {name}")
    print(f"  Code snippet: {code.strip().replace('\n', '  |  ')[:80]}...")
    print(f"  Execution Passed: {execution_result['passed']}")
    print(f"  Detected Mistakes: {mistakes}")
    print(f"  Primary Classification: {primary}")
    print(f"  Expected Mistake: {expected_mistake}")
    print("-" * 60)
    
    return passed

def main():
    print("=" * 60)
    print("Testing Mistake Detector & Classification Model")
    print("=" * 60)
    
    test_cases_sum = [
        {"input": "2\n3", "expected_output": "5"},
        {"input": "10\n20", "expected_output": "30"}
    ]
    
    test_cases_factorial = [
        {"input": "3", "expected_output": "6"},
        {"input": "5", "expected_output": "120"}
    ]

    tests = [
        (
            "Syntax Error",
            """
def add(a, b):
    return a + b
print(add(int(input()), int(input()))
""", # missing closing paren
            test_cases_sum,
            "syntax_error"
        ),
        (
            "Index Error",
            """
arr = [1, 2, 3]
idx = int(input())
print(arr[idx + 10]) # out of range index
""",
            [{"input": "0", "expected_output": "1"}],
            "index_error"
        ),
        (
            "Recursion Error",
            """
def solve(n):
    return solve(n) # infinite recursion
print(solve(int(input())))
""",
            test_cases_factorial,
            "recursion_error"
        ),
        (
            "Logic Error",
            """
def add(a, b):
    return a - b # logic error (subtraction instead of addition)
print(add(int(input()), int(input())))
""",
            test_cases_sum,
            "logic_error"
        ),
        (
            "Potential Missing Base Case",
            """
def recurse(n):
    # recursive call, but no 'if' base case
    return recurse(n - 1)
print(recurse(int(input())))
""",
            test_cases_factorial,
            "potential_missing_base_case"
        ),
        (
            "Shadowing Built-in",
            """
def add(a, b):
    sum = a + b # sum is a built-in function
    return sum
print(add(int(input()), int(input())))
""",
            test_cases_sum,
            "shadowing_builtin"
        ),
        (
            "Invalid Length Method",
            """
arr = [1, 2, 3]
print(arr.length()) # invalid length method
""",
            [{"input": "", "expected_output": "3"}],
            "invalid_len_method"
        ),
        (
            "Invalid Keyword elsif",
            """
x = int(input())
if x > 5:
    print("greater")
elsif x < 5:
    print("lesser")
else:
    print("equal")
""",
            [{"input": "5", "expected_output": "equal"}],
            "invalid_keyword_elsif"
        ),
        (
            "Incorrect None Comparison",
            """
x = None
if x == None:
    print("None!")
else:
    print("Not None")
""",
            [{"input": "", "expected_output": "None!"}],
            "incorrect_none_comparison"
        ),
        (
            "Correct Code (No Mistake)",
            """
def add(a, b):
    return a + b
print(add(int(input()), int(input())))
""",
            test_cases_sum,
            "no_mistake"
        )
    ]
    
    passed_all = True
    for name, code, tc, expected in tests:
        if expected == "no_mistake":
            executor = CodeExecutor()
            res = executor.execute(code, tc)
            analysis = MistakeDetector.analyze_code(code, res)
            
            # Assert no mistakes are detected for correct code
            if len(analysis["mistakes"]) > 0:
                print(f"[FAIL] Test: {name}")
                print(f"  Detected Mistakes: {analysis['mistakes']}")
                passed_all = False
            else:
                print(f"[PASS] Test: {name}")
                print(f"  Detected Mistakes: {analysis['mistakes']}")
                print(f"  Primary Classification: {analysis['primary_mistake']}")
            print("-" * 60)
        else:
            success = run_test_case(name, code, tc, expected)
            if not success:
                passed_all = False
                
    if passed_all:
        print("ALL TESTS PASSED SUCCESSFULLY!")
    else:
        print("SOME TESTS FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
