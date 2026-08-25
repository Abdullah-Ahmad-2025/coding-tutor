# Coding Tutor AI

A full-stack AI-powered coding tutor that goes beyond pass/fail grading. Instead of just telling you whether your code is right or wrong, it figures out *why* you keep making the same mistakes and adapts to teach you better.

Built as an 8-week personal project to explore how machine learning, LLMs, and adaptive systems can work together in a real learning tool.

**Live demo:** [smart-coding-tutor.netlify.app](https://smart-coding-tutor.netlify.app)

---

## What it actually does

When you submit code, three things happen simultaneously:

1. **Your code runs against hidden test cases** in a sandboxed subprocess with a security filter that blocks dangerous imports (`os`, `sys`, `eval`, etc.) and a timeout so infinite loops don't hang the server.

2. **A Naive Bayes classifier** (built from scratch, no ML libraries) analyzes the code and runtime errors to detect 9 specific mistake types — not just "wrong answer", but things like shadowing a built-in, using `.length()` instead of `len()`, missing a recursion base case, or using `== None` instead of `is None`.

3. **Your Mistake DNA profile updates** — a per-user record that tracks how often you make each mistake type and your mastery score (0–100) per topic. The problem recommender reads this profile to figure out what to give you next.

On top of that, you can ask the Groq-powered LLM for a contextual hint or a detailed explanation of a specific mistake — it sees your code, the failing tests, and the detected mistake type, and explains things without just handing you the answer.

---

## Features

- **Monaco Editor** — the same editor as VS Code, with syntax highlighting, line numbers, and auto-indent
- **19 Python problems** across Easy / Medium / Hard, covering basics, loops, recursion, strings, arrays, dictionaries, nested loops, and list comprehensions
- **Mistake DNA dashboard** — conic-gradient mastery rings per topic + colored bar chart of your mistake history
- **Progress tracker** — solved count, total submissions, success rate, and per-topic mastery bars
- **Adaptive recommendations** — picks your next problem based on your weakest topic and appropriate difficulty
- **"Explain My Mistake" button** — per-mistake AI explanations using Llama 3.3 70B via Groq
- **JWT auth** — sign up, log in, stay logged in across sessions
- **Mobile responsive** — sidebar becomes a drawer overlay on small screens
- **Empty code guard** — rejects blank submissions before they hit the executor

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Axios, localStorage |
| Code Editor | Monaco Editor (`@monaco-editor/react`) |
| Backend | FastAPI, Python 3.11, SQLAlchemy ORM, Pydantic |
| Database | PostgreSQL (Railway) |
| AI / LLM | Groq API — `llama-3.3-70b-versatile` via LangChain |
| Auth | JWT (`python-jose`), bcrypt password hashing (`passlib`) |
| Frontend hosting | Netlify |
| Backend hosting | Railway |

---

## Architecture

```
Browser (Netlify)
    │
    │  HTTP + JWT
    ▼
FastAPI Backend (Railway)
    ├── /api/auth          → signup / login → PostgreSQL
    ├── /api/problems      → list, fetch, recommend
    ├── /api/execute       → run code → detect mistakes → update profile
    ├── /api/hints         → Groq LLM hint + explanation
    ├── /api/progress      → per-user stats
    └── /api/mistake-dna   → mastery rings + mistake bars
          │
          ▼
    PostgreSQL (Railway)
    ├── users
    ├── problems (19 seeded)
    ├── submissions
    └── mistake_profiles
```

### How the Mistake Detector works

The detector runs two passes over every submission:

**Pass 1 — Rule-based pattern matching:**
- Regex scans the cleaned code (comments and string literals stripped first to avoid false positives)
- Catches: `.length()` / `.size()`, `elsif`, `== None`, shadowing builtins like `sum = ...`, missing `if` inside recursive functions

**Pass 2 — Naive Bayes classification:**
- Takes the 9 boolean features from Pass 1 as input
- Trained on hand-crafted representative samples with Laplace smoothing
- Outputs a `primary_mistake` label used to drive the "Explain My Mistake" button

Both passes run in under 10ms per submission.

---

## Running Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- A free [Groq API key](https://console.groq.com/)

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/coding-tutor.git
cd coding-tutor

# Backend dependencies
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# or: venv\Scripts\activate    # Windows CMD/PowerShell
# or: source venv/bin/activate # macOS/Linux

pip install -r requirements.txt

# Frontend dependencies
cd frontend && npm install && cd ..
```

### 2. Environment variables

Create a `.env` file in the project root:

```env
# Get yours free at https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here

# Leave this for local SQLite, or swap for a real PostgreSQL URL
DATABASE_URL=sqlite:///./coding_tutor.db

# Any long random string works for local dev
SECRET_KEY=change-this-to-something-secret
```

### 3. Set up the database

```bash
python backend/init_db.py
python backend/seed_problems.py
```

### 4. Start the servers

```bash
# Terminal 1 — backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend
npm start
```

Open [http://localhost:3000](http://localhost:3000), sign up, and start solving.

---

## Deployment

The live version uses:

| Service | What it runs |
|---|---|
| **Railway** | FastAPI backend + PostgreSQL database |
| **Netlify** | React frontend (static build) |

### Environment variables needed on Railway

| Key | Value |
|---|---|
| `DATABASE_URL` | Auto-provided by Railway PostgreSQL plugin |
| `SECRET_KEY` | Any long random string |
| `GROQ_API_KEY` | Your Groq key |

### Environment variables needed on Netlify

| Key | Value |
|---|---|
| `REACT_APP_API_URL` | Your Railway backend URL (e.g. `https://xxx.up.railway.app`) |

### Railway start command

```
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Seeding the production database

After first deploy, run these once locally with your production `DATABASE_URL` in `.env`:

```bash
python backend/init_db.py
python backend/seed_problems.py
```

---

## Running Tests

```bash
# Mistake classifier — verifies all 9 mistake types + correct code
python backend/test_mistake_detector.py

# Integration test — database + execute API end-to-end
python backend/test_api.py
```

Both print `ALL TESTS PASSED SUCCESSFULLY` when everything is working.

---

## Project Structure

```
coding-tutor/
├── backend/
│   ├── main.py                         # FastAPI app, router registration
│   ├── database.py                     # SQLAlchemy engine, session, auto SSL for PostgreSQL
│   ├── init_db.py                      # Creates all tables
│   ├── seed_problems.py                # Seeds 19 Python problems
│   ├── api/
│   │   ├── auth.py                     # POST /signup, /login
│   │   ├── execute.py                  # POST /execute — runs code + updates profile
│   │   ├── hints.py                    # POST /hints/generate, /hints/explain
│   │   ├── mistake_dna.py              # GET /mistake-dna/user/:id
│   │   ├── problems.py                 # GET /problems/, /:id, /recommended/:id
│   │   └── progress.py                 # GET /progress/user/:id
│   ├── models/
│   │   └── schema.py                   # SQLAlchemy models: User, Problem, Submission, MistakeProfile
│   └── services/
│       ├── auth.py                     # JWT creation, bcrypt hashing
│       ├── code_executor.py            # Subprocess runner with security filter + timeout
│       ├── hint_generator.py           # Groq LLM wrapper (hint + explain)
│       ├── knowledge_tracker.py        # Updates mastery scores after each submission
│       ├── mistake_detector.py         # Naive Bayes classifier + regex pattern matcher
│       └── problem_recommender.py      # Picks next problem from weakest topic
├── frontend/
│   └── src/
│       ├── App.js
│       └── pages/
│           └── ProblemPage.jsx         # Entire frontend — editor, sidebar, dashboards, auth
├── requirements.txt
├── Procfile                            # Railway start command
└── .env.example
```

---

## Problems Included

| # | Title | Difficulty | Topic |
|---|---|---|---|
| 1 | Add Two Numbers | Easy | basics |
| 2 | FizzBuzz | Easy | basics |
| 3 | Sum to N | Easy | loops |
| 4 | Count Vowels | Easy | strings |
| 5 | Average of List | Easy | arrays |
| 6 | Factorial | Easy | recursion |
| 7 | Count Character Frequency | Easy | dicts |
| 8 | Find Maximum in List | Medium | arrays |
| 9 | Reverse a String | Medium | strings |
| 10 | Squares of Even Numbers | Medium | arrays |
| 11 | Palindrome Checker | Medium | strings |
| 12 | Multiplication Table | Medium | loops |
| 13 | Merge Two Dictionaries | Medium | dicts |
| 14 | Remove Duplicates | Medium | arrays |
| 15 | Count Primes up to N | Medium | loops |
| 16 | Fibonacci (Nth Term) | Hard | recursion |
| 17 | Matrix Transpose | Hard | arrays |
| 18 | Two Sum | Hard | dicts |
| 19 | Longest Common Prefix | Hard | strings |

---

## Known Limitations

- **Code execution is local to the server** — this works fine on Railway but won't work on serverless platforms like Vercel (no subprocess support)
- **The Naive Bayes classifier is trained on a small hand-crafted dataset** — it works well for the 9 defined mistake types but won't generalize beyond them
- **No rate limiting on the LLM endpoints** — fine for personal/demo use but you'd want to add this before opening it to many users

---

## License

MIT
