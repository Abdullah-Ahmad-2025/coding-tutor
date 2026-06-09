# Coding Tutor AI

**An adaptive AI coding tutor that learns how students learn.**

## 🎯 What It Does

Students write Python code to solve problems. The system:
- Runs their code safely (using local subprocess with timeouts)
- Stores every submission in a database
- Tracks mastery per topic (loops, functions, recursion, etc.)
- Generates personalized hints using Groq LLM
- Recommends next problems based on weak areas

## 🧠 Why This Is Different

Most coding tutors just check pass/fail. This one builds a **Mistake DNA profile** for each student – tracking not just what they got wrong, but *patterns* in their mistakes.

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python) |
| Database | SQLite + SQLAlchemy ORM |
| Code Execution | Local subprocess (sandboxed with timeouts) |
| LLM | Groq API (free tier) |
| Frontend | React (coming soon) |
| Deployment | Railway (planned) |

## 📊 Current Status

| Feature | Status |
|---------|--------|
| Code execution engine | ✅ Complete |
| Database (User, Problem, Submission) | ✅ Complete |
| MistakeProfile tracking | ✅ Complete |
| `/api/execute` endpoint | ✅ Complete |
| LLM hint generation | 🔜 Day 3 |
| Mistake detection | 🔜 Day 3 |
| Frontend UI | 🔜 Day 4-5 |
| Deployment | 🔜 Day 6-7 |

## 🚀 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/coding-tutor.git
cd coding-tutor

# Set up virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
cd backend
python init_db.py
python seed_problems.py

# Run the server
uvicorn backend.main:app --reload