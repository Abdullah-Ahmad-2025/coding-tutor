from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.execute import router as execute_router
from api.problems import router as problems_router
from api.auth import router as auth_router
from api.progress import router as progress_router
from api.mistake_dna import router as mistake_dna_router
from api.hints import router as hints_router

app = FastAPI(title="Coding Tutor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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