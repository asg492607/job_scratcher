from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.opt_out_repo import OptOutRepository

router = APIRouter(prefix="/compliance", tags=["DPDP & Compliance"])

class TakedownRequest(BaseModel):
    company_name: str
    contact_email: Optional[str] = None
    domain: Optional[str] = None
    reason: Optional[str] = "Listing removal request under DPDP / Copyright policy"

@router.post("/takedown", status_code=status.HTTP_201_CREATED)
def submit_takedown_request(
    request: TakedownRequest,
    db: Session = Depends(get_db)
):
    """
    Submits an employer or listing takedown request.
    Registers the company domain/name into the active blocklist and deactivates past listings.
    """
    if not request.company_name or len(request.company_name.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Valid company_name is required for opt-out request."
        )

    repo = OptOutRepository(db)
    opt_out_entry = repo.add_opt_out(
        company_name=request.company_name,
        contact_email=request.contact_email,
        reason=request.reason,
        domain=request.domain
    )

    return {
        "status": "success",
        "message": f"Company '{request.company_name}' has been added to the opt-out list and past listings deactivated.",
        "id": opt_out_entry.id
    }
