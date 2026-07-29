import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Text

from app.database.base import Base

class OptOutCompany(Base):
    """
    Model storing employers or portals that have requested removal / opt-out
    under DPDP Act / copyright guidelines.
    """
    __tablename__ = "opt_out_companies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_name = Column(String, nullable=False, index=True)
    domain = Column(String, nullable=True, index=True)
    reason = Column(Text, nullable=True)
    contact_email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
