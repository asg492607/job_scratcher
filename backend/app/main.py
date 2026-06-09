from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.opportunities import router as opportunities_router
from app.database.session import engine
from app.database.base import Base

# Import models so Base.metadata can find them
import app.models.opportunity
import app.models.skill

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Opportunity Intelligence & Discovery Platform",
    description="API for finding design opportunities",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Should be configurable via env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(opportunities_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to Opportunity Intelligence API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
