import uuid
from database import SessionLocal
from models.schema import Problem

def seed_problems():
    db = SessionLocal()

    # Clear existing
    db.query(Problem).delete()

    problems = [
        {
            "id": "prob_easy_1",
            "title": "Add Two Numbers",
            "description": "Write a function that takes two numbers and returns their sum.",
            "difficulty": "easy",
            "topic": "basics",
            "starter_code": "def add(a, b):\n    # Your code here\n    pass\n\nprint(add(int(input()), int(input())))",
            "test_cases": [
                {"input": "2\n3", "expected_output": "5"},
                {"input": "10\n20", "expected_output": "30"}
            ]
        },
        {
            "id": "prob_easy_2",
            "title": "Sum to N",
            "description": "Write a function that sums integers from 1 to n.",
            "difficulty": "easy",
            "topic": "loops",
            "starter_code": "def sum_to_n(n):\n    # Your code here\n    pass\n\nprint(sum_to_n(int(input())))",
            "test_cases": [
                {"input": "5", "expected_output": "15"},
                {"input": "10", "expected_output": "55"}
            ]
        },
        {
            "id": "prob_easy_3",
            "title": "Factorial",
            "description": "Write a recursive function to calculate factorial.",
            "difficulty": "easy",
            "topic": "recursion",
            "starter_code": "def factorial(n):\n    # Your code here\n    pass\n\nprint(factorial(int(input())))",
            "test_cases": [
                {"input": "5", "expected_output": "120"},
                {"input": "0", "expected_output": "1"},
                {"input": "3", "expected_output": "6"}
            ]
        },
        {
            "id": "prob_medium_1",
            "title": "Find Maximum in List",
            "description": "Find the maximum value in a list.",
            "difficulty": "medium",
            "topic": "arrays",
            "starter_code": "def find_max(lst):\n    # Your code here\n    pass\n\nlst = list(map(int, input().split()))\nprint(find_max(lst))",
            "test_cases": [
                {"input": "1 5 3 9 2", "expected_output": "9"},
                {"input": "10", "expected_output": "10"}
            ]
        },
        {
            "id": "prob_medium_2",
            "title": "Reverse a String",
            "description": "Reverse a string without using built‑in reverse.",
            "difficulty": "medium",
            "topic": "strings",
            "starter_code": "def reverse_string(s):\n    # Your code here\n    pass\n\nprint(reverse_string(input()))",
            "test_cases": [
                {"input": "hello", "expected_output": "olleh"},
                {"input": "abc", "expected_output": "cba"}
            ]
        }
    ]

    for p in problems:
        prob = Problem(**p)
        db.add(prob)

    db.commit()
    print(f"Seeded {len(problems)} problems.")
    db.close()

if __name__ == "__main__":
    seed_problems()