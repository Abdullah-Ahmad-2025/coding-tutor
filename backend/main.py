import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from api.execute import router as execute_router
from api.problems import router as problems_router
from api.auth import router as auth_router
from api.progress import router as progress_router
from api.mistake_dna import router as mistake_dna_router
from api.hints import router as hints_router
from database import SessionLocal, engine
from models.schema import Base
from seed_problems import seed_problems


def get_cors_origins():
    raw_origins = os.getenv("CORS_ALLOWED_ORIGINS", "").strip()
    if raw_origins:
        return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_problems(db=db, replace_existing=False)
    finally:
        db.close()

    yield


cors_origins = get_cors_origins()
allow_all_origins = "*" in cors_origins

app = FastAPI(title="Coding Tutor", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all_origins else cors_origins,
    allow_credentials=not allow_all_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend running"}

app.include_router(execute_router)
app.include_router(problems_router)
app.include_router(auth_router)
app.include_router(progress_router)
app.include_router(mistake_dna_router)
app.include_router(hints_router)
