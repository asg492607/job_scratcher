import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database.base import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False, index=True)

    opportunities = relationship("Opportunity", secondary="opportunity_skills", back_populates="skills")


