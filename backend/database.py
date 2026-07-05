from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Local development fallback: SQLite
    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'coding_tutor.db')}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

elif DATABASE_URL.startswith("sqlite"):
    # Explicit SQLite path (local override)
    db_path = DATABASE_URL[len("sqlite:///"):]
    if not os.path.isabs(db_path):
        DATABASE_URL = f"sqlite:///{os.path.abspath(os.path.join(BASE_DIR, db_path))}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

else:
    # PostgreSQL (Neon, Supabase, Railway, etc.)
    # Neon requires SSL — add sslmode=require if not already present
    if "sslmode" not in DATABASE_URL:
        separator = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL = f"{DATABASE_URL}{separator}sslmode=require"
    engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()