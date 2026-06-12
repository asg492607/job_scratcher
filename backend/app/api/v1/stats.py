from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.session import get_db
from app.models.opportunity import Opportunity

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("")
def get_stats(db: Session = Depends(get_db)):
    """
    Returns monitoring statistics for the Opportunity Intelligence Pipeline.
    """
    total_jobs = db.query(Opportunity).count()
    
    # Jobs per source
    source_counts = db.query(
        Opportunity.source, func.count(Opportunity.id)
    ).group_by(Opportunity.source).all()
    
    sources = {source: count for source, count in source_counts if source}
    
    # Jobs per category (job vs internship vs freelance)
    category_counts = db.query(
        Opportunity.category, func.count(Opportunity.id)
    ).group_by(Opportunity.category).all()
    
    categories = {cat.value if cat else "unknown": count for cat, count in category_counts}
    
    # Jobs per domain
    domain_counts = db.query(
        Opportunity.domain, func.count(Opportunity.id)
    ).group_by(Opportunity.domain).all()
    
    domains = {dom.value if dom else "unknown": count for dom, count in domain_counts}
    
    return {
        "total_jobs_in_database": total_jobs,
        "jobs_per_source": sources,
        "jobs_per_category": categories,
        "jobs_per_domain": domains,
        "pipeline_health": "Healthy"
    }

