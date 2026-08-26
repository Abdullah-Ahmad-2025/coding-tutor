from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


class HintGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment")
        self.llm = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0.7,
            api_key=api_key,
        )

    def generate_hint(
        self,
        problem_description: str,
        user_code: str,
        test_results: list,
        mistakes: list,
    ) -> str:
        """Generate a helpful hint without giving away the answer."""
        failed_tests = [t for t in test_results if not t["passed"]]
        passed_count = sum(1 for t in test_results if t["passed"])
        total_count = len(test_results)

        prompt = f"""You are a helpful programming tutor. A student is working on this problem:

Problem: {problem_description}

The student submitted this code:
```python
{user_code}
```

Test Results:
Passed: {passed_count}/{total_count}
Failed tests: {failed_tests}

Detected issues: {mistakes}

Give a SHORT (2-3 sentences) HINT that helps the student fix their code.
DO NOT provide the solution or complete code.
Focus on: What concept might they be missing? What should they think about?

Hint:"""

        response = self.llm.invoke(prompt)
        return response.content

    def explain_mistake(
        self,
        problem_description: str,
        user_code: str,
        test_results: list,
        mistake_type: str,
    ) -> str:
        """Explain a specific type of mistake in detail."""
        prompt = f"""You are a programming tutor explaining a student's mistake.

Problem: {problem_description}

Student Code:
```python
{user_code}
```

Test Results: {test_results}

Mistake Type: {mistake_type}

Explain what went wrong and why, in 3-4 sentences. Then suggest how to fix it (without giving the full solution).

Explanation:"""

        response = self.llm.invoke(prompt)
        return response.content
