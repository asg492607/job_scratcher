import os

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.opportunities import router as opportunities_router
from app.api.v1.stats import router as stats_router
from app.database.session import SessionLocal, engine
from app.database.base import Base
from app.services.scraping_service import ScrapingService

# Import models so Base.metadata can find them
import app.models.opportunity
import app.models.skill

Base.metadata.create_all(bind=engine)

scheduler = BackgroundScheduler()

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
app.include_router(stats_router, prefix="/api/v1")

def run_scheduled_scrape():
    db = SessionLocal()
    try:
        ScrapingService(db).scrape_all()
    finally:
        db.close()

@app.on_event("startup")
def start_scheduler():
    if os.getenv("ENABLE_BACKGROUND_SCRAPING", "true").lower() != "true":
        return

    interval_minutes = int(os.getenv("SCRAPE_INTERVAL_MINUTES", "360"))
    scheduler.add_job(
        run_scheduled_scrape,
        "interval",
        minutes=interval_minutes,
        id="scrape_design_opportunities",
        replace_existing=True,
    )
    scheduler.start()

@app.on_event("shutdown")
def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()

from fastapi.staticfiles import StaticFiles

# Mount the static files (vanilla HTML/CSS/JS frontend)
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

