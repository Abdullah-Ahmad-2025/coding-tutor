# Coding Tutor AI

**An adaptive, intelligent programming tutor that analyzes how students learn by building a personalized "Mistake DNA" profile.**

---

## 🎯 System Architecture Diagram

```mermaid
graph TD
    subgraph Frontend [React Application]
        UI[ProblemPage Component]
        Monaco[Monaco Code Editor]
        AuthForm[JWT Login/Signup Modal]
        Dashboards[Progress & Mistake DNA Dashboards]
    end

    subgraph Backend [FastAPI Application]
        API[API Endpoints]
        Exec[Code Executor Service]
        Detect[Naive Bayes Mistake Detector]
        Track[Knowledge Tracker]
        Rec[Problem Recommender]
        LLM[Groq Hint Generator]
    end

    subgraph DB [SQLite Database]
        UsersTable[(Users Table)]
        ProblemsTable[(Problems Table)]
        SubmissionsTable[(Submissions Table)]
        ProfilesTable[(Mistake Profiles Table)]
    end

    UI --> Monaco
    UI --> AuthForm
    UI --> Dashboards

    UI -- HTTP Requests with JWT --> API
    API --> Exec
    API --> Detect
    API --> Track
    API --> Rec
    API --> LLM

    Exec -- Local Subprocess --> SandboxedRun[Safety Scanned Python Execution]
    Track --> DB
    Rec --> DB
    API --> DB
```

---

## 🛠️ Key Features

1. **Monaco Editor Integration:** Full Python coding workspace featuring line numbers, auto-indentation, and syntax highlighting matching industry standards.
2. **Mistake DNA Profiling:** Custom-built Naive Bayes Classifier that detects 9 distinct types of structural or algorithmic mistakes (e.g., shadowing built-ins, infinite recursion, missing base cases, invalid length methods) instead of just checking pass/fail.
3. **Adaptive Recommendations:** The recommender calculates weaknesses across all topics and dynamically selects the next appropriate problem and difficulty level.
4. **Context-Aware AI Hints:** Integrates with the Groq Llama 3 LLM service to analyze code and failing tests, generating 2-3 sentence hints without exposing the solution.
5. **Secure Local Executor:** Python execution environment sandboxed with timeouts and a security scan filter blocking restricted imports (e.g. `os`, `sys`, `subprocess`, `eval`).
6. **JWT Authentication:** Complete user registration, login, and secure session state persisted in `localStorage`.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React (Hooks, Axios, LocalStorage) |
| **Code Editor** | Monaco Editor (`@monaco-editor/react`) |
| **Backend** | FastAPI (Python 3.11, Pydantic, SQLAlchemy ORM) |
| **Database** | SQLite |
| **AI / LLM** | Groq API (`llama-3.3-70b-versatile`) |
| **Authentication** | JWT Tokens (`python-jose`) & Password Hashing (`bcrypt` + `passlib`) |

---

## 🚀 How to Set Up & Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/coding-tutor.git
cd coding-tutor
```

### 2. Configure the Backend (Python)
Navigate to the root directory and set up a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the root directory (you can copy `.env.example` as a template):
```env
# Groq API Key (Obtain from https://console.groq.com/ for free)
GROQ_API_KEY=your_groq_api_key_here

# Database URI (Defaults to local SQLite)
DATABASE_URL=sqlite:///./coding_tutor.db

# JWT Secret Key
SECRET_KEY=your-super-secret-key-change-in-production
```

### 3. Initialize and Seed the Database
From the project root:
```bash
python backend/init_db.py
python backend/seed_problems.py
```

### 4. Run the Backend Server
```bash
uvicorn backend.main:app --reload --port 8000
```

### 5. Run the Frontend (React)
Open a new terminal session, navigate to the `frontend` folder, and start the development server:

```bash
cd frontend

# Install Node modules
npm install

# Start React app
npm start
```
The React development server will start at `http://localhost:3000`.

---

## 🧪 Running Automated Tests
The project features an automated suite of tests for both the code runner and the machine learning mistake classifier.

To run the classifier verification tests:
```bash
python backend/test_mistake_detector.py
```

To run the API and database integration tests:
```bash
python backend/test_api.py
```