import subprocess
import tempfile
import os
import signal
import time
from typing import Dict, List, Any

class CodeExecutor:
    """A secure local code executor using subprocess with strict limits."""

    def __init__(self, timeout_seconds: int = 5):
        self.timeout = timeout_seconds

    def execute(self, code: str, test_cases: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Execute Python code against test cases using a local subprocess.

        test_cases: [{"input": "5", "expected_output": "120"}, ...]
        """
        results = []
        passed_count = 0

        for test in test_cases:
            try:
                # Create a temporary file for the user's code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(code)
                    temp_file = f.name

                # Run the script with the test input
                start_time = time.time()
                process = subprocess.run(
                    ['python', temp_file],
                    input=test["input"],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
                execution_time = time.time() - start_time

                # Clean up the temporary file
                os.unlink(temp_file)

                output = process.stdout.strip()
                error = process.stderr.strip()

                passed = (output == test["expected_output"])

                if passed:
                    passed_count += 1

                results.append({
                    "input": test["input"],
                    "expected": test["expected_output"],
                    "actual": output,
                    "passed": passed,
                    "status": "Accepted" if passed else "Wrong Answer",
                    "execution_time": round(execution_time, 3),
                    "error": error if error else None
                })

            except subprocess.TimeoutExpired:
                results.append({
                    "input": test["input"],
                    "expected": test["expected_output"],
                    "actual": "",
                    "passed": False,
                    "status": "Timeout: Code execution exceeded limit",
                    "execution_time": self.timeout
                })
            except Exception as e:
                results.append({
                    "input": test["input"],
                    "expected": test["expected_output"],
                    "actual": "",
                    "passed": False,
                    "status": f"Execution error: {str(e)}"
                })

        all_passed = (passed_count == len(test_cases))

        return {
            "results": results,
            "passed": all_passed,
            "passed_count": passed_count,
            "total_count": len(test_cases)
        }