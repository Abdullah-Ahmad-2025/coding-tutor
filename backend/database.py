from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'coding_tutor.db')}"
elif DATABASE_URL.startswith("sqlite:///"):
    db_path = DATABASE_URL[10:]
    if db_path.startswith("./"):
        db_path = db_path[2:]
    if not os.path.isabs(db_path):
        DATABASE_URL = f"sqlite:///{os.path.abspath(os.path.join(BASE_DIR, db_path))}"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session (for FastAPI routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()