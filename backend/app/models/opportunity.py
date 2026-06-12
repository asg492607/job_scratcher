import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Table
from sqlalchemy.orm import relationship
import enum

from app.database.base import Base

class RemoteStatus(str, enum.Enum):
    remote = "remote"
    hybrid = "hybrid"
    onsite = "onsite"

class OpportunityCategory(str, enum.Enum):
    internship = "internship"
    job = "job"
    hackathon = "hackathon"
    fellowship = "fellowship"
    competition = "competition"
    freelance = "freelance"

class OpportunityDomain(str, enum.Enum):
    ux_ui = "ux_ui"
    graphic_design = "graphic_design"
    product_design = "product_design"
    motion_graphics = "motion_graphics"
    industrial_design = "industrial_design"
    architecture = "architecture"
    other = "other"

class DifficultyLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

opportunity_skills = Table(
    "opportunity_skills",
    Base.metadata,
    Column("opportunity_id", String, ForeignKey("opportunities.id"), primary_key=True),
    Column("skill_id", String, ForeignKey("skills.id"), primary_key=True)
)

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    company = Column(String, nullable=True)
    normalized_company = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    remote_status = Column(SQLEnum(RemoteStatus), nullable=True)
    salary = Column(String, nullable=True)
    min_salary = Column(Float, nullable=True)
    max_salary = Column(Float, nullable=True)
    currency = Column(String, nullable=True)
    stipend = Column(String, nullable=True)
    experience_level = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)
    source = Column(String, nullable=True)
    apply_url = Column(String, nullable=True)
    
    category = Column(SQLEnum(OpportunityCategory), nullable=True)
    domain = Column(SQLEnum(OpportunityDomain), nullable=True)
    difficulty = Column(SQLEnum(DifficultyLevel), nullable=True)
    industry = Column(String, nullable=True)
    
    quality_score = Column(Float, nullable=True)
    freshness_score = Column(Float, nullable=True)
    source_reliability_score = Column(Float, nullable=True)
    
    growth_potential = Column(Text, nullable=True)
    portfolio_required = Column(Boolean, default=False)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    skills = relationship("Skill", secondary=opportunity_skills, back_populates="opportunities")


