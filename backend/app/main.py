import os
import sys
from contextlib import asynccontextmanager

# Ensure backend directory is in sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from dotenv import load_dotenv
import uvicorn

load_dotenv()

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

try:
    from app.api.v1.opportunities import router as opportunities_router
    from app.api.v1.stats import router as stats_router
    from app.database.session import SessionLocal, engine
    from app.database.base import Base
    from app.services.scraping_service import ScrapingService
    import app.models
except ImportError:
    from .api.v1.opportunities import router as opportunities_router
    from .api.v1.stats import router as stats_router
    from .database.session import SessionLocal, engine
    from .database.base import Base
    from .services.scraping_service import ScrapingService
    from . import models

Base.metadata.create_all(bind=engine)

scheduler = BackgroundScheduler()


def run_scheduled_scrape():
    db = SessionLocal()
    try:
        ScrapingService(db).scrape_all()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("ENABLE_BACKGROUND_SCRAPING", "true").lower() == "true":
        interval_minutes = int(os.getenv("SCRAPE_INTERVAL_MINUTES", "360"))
        scheduler.add_job(
            run_scheduled_scrape,
            "interval",
            minutes=interval_minutes,
            id="scrape_design_opportunities",
            replace_existing=True,
        )
        scheduler.start()
    yield
    if scheduler.running:
        scheduler.shutdown()


app = FastAPI(
    title="Opportunity Intelligence & Discovery Platform",
    description="API for finding design opportunities",
    version="1.0.0",
    lifespan=lifespan,
)

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(opportunities_router, prefix="/api/v1")
app.include_router(stats_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Mount the static files (vanilla HTML/CSS/JS frontend)
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
