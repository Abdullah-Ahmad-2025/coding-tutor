from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.execute import router

# Create the FastAPI application
app = FastAPI(title="Coding Tutor")

# Allow requests from any origin (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a simple health check endpoint
@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend running"}

app.include_router(router)

# If you run this file directly, start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)