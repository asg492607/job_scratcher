import os

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.opportunities import router as opportunities_router
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
from fastapi.responses import FileResponse

# Mount the static files (assets, js, css)
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(static_path):
    assets_path = os.path.join(static_path, "assets")
    if os.path.isdir(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

    # Serve index.html for all non-API routes (React Router support)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            return {"error": "Not Found"}
            
        # Check if requesting a static file from the root of dist (e.g. favicon.ico)
        requested_file = os.path.join(static_path, full_path)
        if os.path.isfile(requested_file):
            return FileResponse(requested_file)
            
        index_file = os.path.join(static_path, "index.html")
        if os.path.isfile(index_file):
            return FileResponse(index_file)
        return {"error": "Frontend not built"}
else:
    @app.get("/")
    def read_root():
        return {"status": "ok", "message": "Welcome to Opportunity Intelligence API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
