from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):

    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)   # added this line for storing hashed password
    created_at = Column(DateTime, default=datetime.utcnow)

class Problem(Base):

    __tablename__ = "problems"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String)  # easy, medium, hard
    topic = Column(String)       # loops, functions, recursion, arrays, dicts
    starter_code = Column(Text)
    test_cases = Column(JSON)    # [{"input": "5", "expected": "120"}, ...]
    created_at = Column(DateTime, default=datetime.utcnow)

class Submission(Base):

    __tablename__ = "submissions"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    problem_id = Column(String, ForeignKey("problems.id"), nullable=False)
    code = Column(Text, nullable=False)
    passed = Column(Boolean, default=False)      # True if all tests pass
    passed_count = Column(Integer, default=0)    # How many tests passed
    total_count = Column(Integer, default=0)     # Total tests
    created_at = Column(DateTime, default=datetime.utcnow)

class MistakeProfile(Base):

    __tablename__ = "mistake_profiles"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)

    # Knowledge state (0-100 scale)
    loops_mastery = Column(Integer, default=0)
    functions_mastery = Column(Integer, default=0)
    recursion_mastery = Column(Integer, default=0)
    arrays_mastery = Column(Integer, default=0)
    dicts_mastery = Column(Integer, default=0)

    # Mistake DNA counters!
    syntax_errors = Column(Integer, default=0)
    index_errors = Column(Integer, default=0)
    logic_errors = Column(Integer, default=0)
    recursion_errors = Column(Integer, default=0)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)