from typing import Optional
from sqlalchemy.orm import Session
from app.models.opt_out import OptOutCompany

class OptOutRepository:
    """
    Repository for managing blocked employers / opt-out listings under compliance policies.
    """
    def __init__(self, db: Session):
        self.db = db

    def is_company_blocked(self, company_name: Optional[str]) -> bool:
        """
        Checks if a company name is on the active opt-out blocklist.
        """
        if not company_name:
            return False

        normalized_target = company_name.strip().lower()
        
        # Exact or partial match check
        existing = (
            self.db.query(OptOutCompany)
            .filter(OptOutCompany.is_active == True)
            .all()
        )

        for entry in existing:
            if entry.company_name.strip().lower() in normalized_target or normalized_target in entry.company_name.strip().lower():
                return True

        return False

    def add_opt_out(self, company_name: str, contact_email: Optional[str] = None, reason: Optional[str] = None, domain: Optional[str] = None) -> OptOutCompany:
        """
        Registers an employer opt-out request.
        """
        entry = OptOutCompany(
            company_name=company_name,
            contact_email=contact_email,
            reason=reason,
            domain=domain,
            is_active=True
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)

        # Deactivate any past opportunities for this company
        from app.models.opportunity import Opportunity
        self.db.query(Opportunity).filter(
            Opportunity.company.ilike(f"%{company_name}%")
        ).update({"is_active": False}, synchronize_session=False)
        self.db.commit()

        return entry
