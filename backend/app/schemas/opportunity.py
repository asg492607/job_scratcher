from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.opportunity import RemoteStatus, OpportunityCategory, OpportunityDomain, DifficultyLevel

class SkillBase(BaseModel):
    name: str

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: str

    class Config:
        from_attributes = True

class OpportunityBase(BaseModel):
    title: str
    company: Optional[str] = None
    normalized_company: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    remote_status: Optional[RemoteStatus] = None
    salary: Optional[str] = None
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    currency: Optional[str] = None
    stipend: Optional[str] = None
    experience_level: Optional[str] = None
    deadline: Optional[datetime] = None
    source: Optional[str] = None
    apply_url: Optional[str] = None
    category: Optional[OpportunityCategory] = None
    domain: Optional[OpportunityDomain] = None
    difficulty: Optional[DifficultyLevel] = None
    industry: Optional[str] = None
    quality_score: Optional[float] = None
    freshness_score: Optional[float] = None
    source_reliability_score: Optional[float] = None
    growth_potential: Optional[str] = None
    portfolio_required: bool = False
    is_active: bool = True

class OpportunityCreate(OpportunityBase):
    skills: List[str] = [] # list of skill names

class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    normalized_company: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    remote_status: Optional[RemoteStatus] = None
    salary: Optional[str] = None
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    currency: Optional[str] = None
    stipend: Optional[str] = None
    experience_level: Optional[str] = None
    deadline: Optional[datetime] = None
    source: Optional[str] = None
    apply_url: Optional[str] = None
    category: Optional[OpportunityCategory] = None
    domain: Optional[OpportunityDomain] = None
    difficulty: Optional[DifficultyLevel] = None
    industry: Optional[str] = None
    quality_score: Optional[float] = None
    freshness_score: Optional[float] = None
    source_reliability_score: Optional[float] = None
    growth_potential: Optional[str] = None
    portfolio_required: Optional[bool] = None
    is_active: Optional[bool] = None
    skills: Optional[List[str]] = None

class OpportunityResponse(OpportunityBase):
    id: str
    created_at: datetime
    updated_at: datetime
    skills: List[SkillResponse] = []

    class Config:
        from_attributes = True

