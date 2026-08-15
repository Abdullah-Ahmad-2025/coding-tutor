import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models.schema import Problem


def seed_problems(db=None, replace_existing=True):
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    if replace_existing:
        db.query(Problem).delete()
    elif db.query(Problem).first():
        if owns_session:
            db.close()
        return 0

    problems = [
        # ─────────────── EASY ───────────────
        {
            "id": "prob_easy_1",
            "title": "Add Two Numbers",
            "description": "Write a function that takes two integers and returns their sum.\n\nExample:\nInput: 2 3\nOutput: 5",
            "difficulty": "easy",
            "topic": "basics",
            "starter_code": "def add(a, b):\n    # Your code here\n    pass\n\nprint(add(int(input()), int(input())))",
            "test_cases": [
                {"input": "2\n3", "expected_output": "5"},
                {"input": "10\n20", "expected_output": "30"},
                {"input": "-1\n1", "expected_output": "0"},
            ],
        },
        {
            "id": "prob_easy_2",
            "title": "Sum to N",
            "description": "Write a function that sums integers from 1 to n (inclusive).\n\nExample:\nInput: 5\nOutput: 15",
            "difficulty": "easy",
            "topic": "loops",
            "starter_code": "def sum_to_n(n):\n    # Your code here\n    pass\n\nprint(sum_to_n(int(input())))",
            "test_cases": [
                {"input": "5", "expected_output": "15"},
                {"input": "10", "expected_output": "55"},
                {"input": "1", "expected_output": "1"},
            ],
        },
        {
            "id": "prob_easy_3",
            "title": "Factorial",
            "description": "Write a recursive function to calculate n! (factorial).\n\nExample:\nInput: 5\nOutput: 120",
            "difficulty": "easy",
            "topic": "recursion",
            "starter_code": "def factorial(n):\n    # Your code here\n    pass\n\nprint(factorial(int(input())))",
            "test_cases": [
                {"input": "5", "expected_output": "120"},
                {"input": "0", "expected_output": "1"},
                {"input": "3", "expected_output": "6"},
            ],
        },
        {
            "id": "prob_easy_4",
            "title": "Count Vowels",
            "description": "Count the number of vowels (a, e, i, o, u) in a string. Case-insensitive.\n\nExample:\nInput: Hello World\nOutput: 3",
            "difficulty": "easy",
            "topic": "strings",
            "starter_code": "def count_vowels(s):\n    # Your code here\n    pass\n\nprint(count_vowels(input()))",
            "test_cases": [
                {"input": "Hello World", "expected_output": "3"},
                {"input": "Python", "expected_output": "1"},
                {"input": "aeiou", "expected_output": "5"},
                {"input": "rhythm", "expected_output": "0"},
            ],
        },
        {
            "id": "prob_easy_5",
            "title": "Average of List",
            "description": "Given a space-separated list of numbers, compute the average rounded to 2 decimal places.\n\nExample:\nInput: 1 2 3 4 5\nOutput: 3.0",
            "difficulty": "easy",
            "topic": "arrays",
            "starter_code": "def average(lst):\n    # Your code here\n    pass\n\nnums = list(map(float, input().split()))\nprint(average(nums))",
            "test_cases": [
                {"input": "1 2 3 4 5", "expected_output": "3.0"},
                {"input": "10 20", "expected_output": "15.0"},
                {"input": "7", "expected_output": "7.0"},
            ],
        },
        {
            "id": "prob_easy_6",
            "title": "FizzBuzz",
            "description": "Print numbers from 1 to n. For multiples of 3 print 'Fizz', for multiples of 5 print 'Buzz', for multiples of both print 'FizzBuzz'.\n\nExample:\nInput: 5\nOutput (one per line):\n1\n2\nFizz\n4\nBuzz",
            "difficulty": "easy",
            "topic": "basics",
            "starter_code": "def fizzbuzz(n):\n    for i in range(1, n+1):\n        # Your code here\n        pass\n\nfizzbuzz(int(input()))",
            "test_cases": [
                {"input": "5", "expected_output": "1\n2\nFizz\n4\nBuzz"},
                {"input": "3", "expected_output": "1\n2\nFizz"},
                {"input": "15", "expected_output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"},
            ],
        },
        {
            "id": "prob_easy_7",
            "title": "Count Character Frequency",
            "description": "Given a string, return each unique character and how many times it appears, sorted alphabetically by character.\n\nFormat: 'char:count' per line.\n\nExample:\nInput: hello\nOutput:\ne:1\nh:1\nl:2\no:1",
            "difficulty": "easy",
            "topic": "dicts",
            "starter_code": "def char_freq(s):\n    # Your code here\n    pass\n\nresult = char_freq(input())\nfor char, count in sorted(result.items()):\n    print(f'{char}:{count}')",
            "test_cases": [
                {"input": "hello", "expected_output": "e:1\nh:1\nl:2\no:1"},
                {"input": "aab", "expected_output": "a:2\nb:1"},
                {"input": "z", "expected_output": "z:1"},
            ],
        },
        # ─────────────── MEDIUM ───────────────
        {
            "id": "prob_medium_1",
            "title": "Find Maximum in List",
            "description": "Find the maximum value in a list without using Python's built-in max().\n\nExample:\nInput: 1 5 3 9 2\nOutput: 9",
            "difficulty": "medium",
            "topic": "arrays",
            "starter_code": "def find_max(lst):\n    # Your code here (don't use max())\n    pass\n\nlst = list(map(int, input().split()))\nprint(find_max(lst))",
            "test_cases": [
                {"input": "1 5 3 9 2", "expected_output": "9"},
                {"input": "10", "expected_output": "10"},
                {"input": "-3 -1 -4 -2", "expected_output": "-1"},
            ],
        },
        {
            "id": "prob_medium_2",
            "title": "Reverse a String",
            "description": "Reverse a string without using Python's built-in reverse or slicing [::-1].\n\nExample:\nInput: hello\nOutput: olleh",
            "difficulty": "medium",
            "topic": "strings",
            "starter_code": "def reverse_string(s):\n    # Your code here (no slicing [::-1])\n    pass\n\nprint(reverse_string(input()))",
            "test_cases": [
                {"input": "hello", "expected_output": "olleh"},
                {"input": "abc", "expected_output": "cba"},
                {"input": "a", "expected_output": "a"},
            ],
        },
        {
            "id": "prob_medium_3",
            "title": "Squares of Even Numbers",
            "description": "Given a list of space-separated integers, return a space-separated list of squares of only the even numbers, using a list comprehension.\n\nExample:\nInput: 1 2 3 4 5 6\nOutput: 4 16 36",
            "difficulty": "medium",
            "topic": "arrays",
            "starter_code": "nums = list(map(int, input().split()))\n# Use a list comprehension to get squares of even numbers\nresult = []  # Replace with list comprehension\nprint(' '.join(map(str, result)))",
            "test_cases": [
                {"input": "1 2 3 4 5 6", "expected_output": "4 16 36"},
                {"input": "2 4 6", "expected_output": "4 16 36"},
                {"input": "1 3 5", "expected_output": ""},
            ],
        },
        {
            "id": "prob_medium_4",
            "title": "Palindrome Checker",
            "description": "Determine if a string is a palindrome (reads the same forwards and backwards). Ignore case.\n\nPrint True or False.\n\nExample:\nInput: racecar\nOutput: True",
            "difficulty": "medium",
            "topic": "strings",
            "starter_code": "def is_palindrome(s):\n    # Your code here\n    pass\n\nprint(is_palindrome(input()))",
            "test_cases": [
                {"input": "racecar", "expected_output": "True"},
                {"input": "hello", "expected_output": "False"},
                {"input": "Madam", "expected_output": "True"},
                {"input": "a", "expected_output": "True"},
            ],
        },
        {
            "id": "prob_medium_5",
            "title": "Multiplication Table",
            "description": "Print the multiplication table for a given number n, from 1 to 10 (using nested loops).\n\nExample:\nInput: 3\nOutput:\n3 x 1 = 3\n3 x 2 = 6\n...\n3 x 10 = 30",
            "difficulty": "medium",
            "topic": "loops",
            "starter_code": "n = int(input())\n# Use nested loops or a loop to print the multiplication table\nfor i in range(1, 11):\n    # Your code here\n    pass",
            "test_cases": [
                {"input": "3", "expected_output": "3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15\n3 x 6 = 18\n3 x 7 = 21\n3 x 8 = 24\n3 x 9 = 27\n3 x 10 = 30"},
                {"input": "5", "expected_output": "5 x 1 = 5\n5 x 2 = 10\n5 x 3 = 15\n5 x 4 = 20\n5 x 5 = 25\n5 x 6 = 30\n5 x 7 = 35\n5 x 8 = 40\n5 x 9 = 45\n5 x 10 = 50"},
            ],
        },
        {
            "id": "prob_medium_6",
            "title": "Merge Two Dictionaries",
            "description": "Given two lines of key=value pairs, merge them into one dictionary. If a key appears in both, sum the values. Print sorted by key.\n\nExample:\nInput:\na=1 b=2\nb=3 c=4\nOutput:\na:1\nb:5\nc:4",
            "difficulty": "medium",
            "topic": "dicts",
            "starter_code": "line1 = input().split()\nline2 = input().split()\nd1 = {k: int(v) for k, v in (pair.split('=') for pair in line1)}\nd2 = {k: int(v) for k, v in (pair.split('=') for pair in line2)}\n# Merge d1 and d2 here, sum values for duplicate keys\nmerged = {}\n# Your code here\nfor k in sorted(merged):\n    print(f'{k}:{merged[k]}')",
            "test_cases": [
                {"input": "a=1 b=2\nb=3 c=4", "expected_output": "a:1\nb:5\nc:4"},
                {"input": "x=10\ny=20", "expected_output": "x:10\ny:20"},
                {"input": "a=5 b=5\na=5 b=5", "expected_output": "a:10\nb:10"},
            ],
        },
        {
            "id": "prob_medium_7",
            "title": "Remove Duplicates",
            "description": "Given a space-separated list of integers, remove duplicates while preserving the original order.\n\nExample:\nInput: 3 1 4 1 5 9 2 6 5 3\nOutput: 3 1 4 5 9 2 6",
            "difficulty": "medium",
            "topic": "arrays",
            "starter_code": "def remove_duplicates(lst):\n    # Your code here (preserve order)\n    pass\n\nnums = list(map(int, input().split()))\nprint(' '.join(map(str, remove_duplicates(nums))))",
            "test_cases": [
                {"input": "3 1 4 1 5 9 2 6 5 3", "expected_output": "3 1 4 5 9 2 6"},
                {"input": "1 1 1", "expected_output": "1"},
                {"input": "1 2 3", "expected_output": "1 2 3"},
            ],
        },
        {
            "id": "prob_medium_8",
            "title": "Count Primes up to N",
            "description": "Count how many prime numbers exist from 2 to n (inclusive).\n\nExample:\nInput: 10\nOutput: 4   (primes: 2, 3, 5, 7)",
            "difficulty": "medium",
            "topic": "loops",
            "starter_code": "def count_primes(n):\n    count = 0\n    for num in range(2, n+1):\n        # Use a nested loop to check if num is prime\n        pass\n    return count\n\nprint(count_primes(int(input())))",
            "test_cases": [
                {"input": "10", "expected_output": "4"},
                {"input": "2", "expected_output": "1"},
                {"input": "1", "expected_output": "0"},
                {"input": "20", "expected_output": "8"},
            ],
        },
        # ─────────────── HARD ───────────────
        {
            "id": "prob_hard_1",
            "title": "Fibonacci (Nth Term)",
            "description": "Return the nth Fibonacci number using recursion. F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).\n\nExample:\nInput: 7\nOutput: 13",
            "difficulty": "hard",
            "topic": "recursion",
            "starter_code": "def fibonacci(n):\n    # Your recursive code here\n    pass\n\nprint(fibonacci(int(input())))",
            "test_cases": [
                {"input": "7", "expected_output": "13"},
                {"input": "0", "expected_output": "0"},
                {"input": "1", "expected_output": "1"},
                {"input": "10", "expected_output": "55"},
            ],
        },
        {
            "id": "prob_hard_2",
            "title": "Matrix Transpose",
            "description": "Transpose an NxM matrix. Input: first line is N (rows) and M (cols), then N lines each with M space-separated integers.\n\nExample:\nInput:\n2 3\n1 2 3\n4 5 6\nOutput:\n1 4\n2 5\n3 6",
            "difficulty": "hard",
            "topic": "arrays",
            "starter_code": "n, m = map(int, input().split())\nmatrix = [list(map(int, input().split())) for _ in range(n)]\n# Transpose the matrix using nested loops or list comprehension\ntransposed = []\n# Your code here\nfor row in transposed:\n    print(' '.join(map(str, row)))",
            "test_cases": [
                {"input": "2 3\n1 2 3\n4 5 6", "expected_output": "1 4\n2 5\n3 6"},
                {"input": "1 3\n7 8 9", "expected_output": "7\n8\n9"},
                {"input": "3 3\n1 2 3\n4 5 6\n7 8 9", "expected_output": "1 4 7\n2 5 8\n3 6 9"},
            ],
        },
        {
            "id": "prob_hard_3",
            "title": "Two Sum",
            "description": "Given a list of integers and a target, find the indices of the two numbers that add up to the target. Print them space-separated (smaller index first). Guaranteed exactly one solution.\n\nInput line 1: space-separated numbers\nInput line 2: target\n\nExample:\nInput:\n2 7 11 15\n9\nOutput: 0 1",
            "difficulty": "hard",
            "topic": "dicts",
            "starter_code": "nums = list(map(int, input().split()))\ntarget = int(input())\n# Use a dictionary to find two indices that sum to target\n# Your code here",
            "test_cases": [
                {"input": "2 7 11 15\n9", "expected_output": "0 1"},
                {"input": "3 2 4\n6", "expected_output": "1 2"},
                {"input": "1 5 3 7\n8", "expected_output": "1 3"},
            ],
        },
        {
            "id": "prob_hard_4",
            "title": "Longest Common Prefix",
            "description": "Find the longest common prefix string among a list of space-separated words. If there is no common prefix, return an empty string (print nothing).\n\nExample:\nInput: flower flow flight\nOutput: fl",
            "difficulty": "hard",
            "topic": "strings",
            "starter_code": "def longest_common_prefix(words):\n    # Your code here\n    pass\n\nwords = input().split()\nresult = longest_common_prefix(words)\nprint(result)",
            "test_cases": [
                {"input": "flower flow flight", "expected_output": "fl"},
                {"input": "dog racecar car", "expected_output": ""},
                {"input": "interview intercom", "expected_output": "inter"},
                {"input": "apple", "expected_output": "apple"},
            ],
        },
    ]

    for p in problems:
        prob = Problem(**p)
        db.add(prob)

    db.commit()
    print(f"Seeded {len(problems)} problems successfully.")

    if owns_session:
        db.close()

    return len(problems)


if __name__ == "__main__":
    seed_problems()
