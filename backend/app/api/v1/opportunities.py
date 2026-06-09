from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.schemas.opportunity import OpportunityResponse, OpportunityCreate, OpportunityUpdate
from app.repositories.opportunity_repo import OpportunityRepository
from app.services.scraping_service import ScrapingService

router = APIRouter(prefix="/opportunities", tags=["opportunities"])

def get_repo(db: Session = Depends(get_db)):
    return OpportunityRepository(db)

def get_scraping_service(db: Session = Depends(get_db)):
    return ScrapingService(db)

@router.get("/", response_model=List[OpportunityResponse])
def get_opportunities(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[List[str]] = None,
    remote_status: Optional[List[str]] = None,
    domain: Optional[List[str]] = None,
    difficulty: Optional[List[str]] = None,
    portfolio_required: Optional[bool] = None,
    repo: OpportunityRepository = Depends(get_repo),
):
    return repo.get_all(
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        remote_status=remote_status,
        domain=domain,
        difficulty=difficulty,
        portfolio_required=portfolio_required,
    )

@router.post("/scrape")
def scrape_opportunities(service: ScrapingService = Depends(get_scraping_service)):
    return service.scrape_all()

@router.post("/scrape/{source}")
def scrape_source(source: str, service: ScrapingService = Depends(get_scraping_service)):
    return service.scrape_source(source)

@router.get("/{opp_id}", response_model=OpportunityResponse)
def get_opportunity(opp_id: str, repo: OpportunityRepository = Depends(get_repo)):
    opp = repo.get_by_id(opp_id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opp

@router.post("/", response_model=OpportunityResponse, status_code=201)
def create_opportunity(opp: OpportunityCreate, repo: OpportunityRepository = Depends(get_repo)):
    return repo.create(opp)

@router.put("/{opp_id}", response_model=OpportunityResponse)
def update_opportunity(opp_id: str, opp: OpportunityUpdate, repo: OpportunityRepository = Depends(get_repo)):
    updated = repo.update(opp_id, opp)
    if not updated:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return updated

@router.delete("/{opp_id}", status_code=204)
def delete_opportunity(opp_id: str, repo: OpportunityRepository = Depends(get_repo)):
    deleted = repo.delete(opp_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Opportunity not found")
