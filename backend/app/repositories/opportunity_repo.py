from sqlalchemy.orm import Session
from app.models.opportunity import Opportunity
from app.models.skill import Skill
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate

class OpportunityRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Opportunity).offset(skip).limit(limit).all()

    def get_by_id(self, opp_id: str):
        return self.db.query(Opportunity).filter(Opportunity.id == opp_id).first()

    def _get_or_create_skills(self, skill_names: list[str]):
        skills = []
        for name in skill_names:
            skill = self.db.query(Skill).filter(Skill.name == name).first()
            if not skill:
                skill = Skill(name=name)
                self.db.add(skill)
            skills.append(skill)
        return skills

    def create(self, opp_data: OpportunityCreate):
        data = opp_data.dict(exclude={"skills"})
        new_opp = Opportunity(**data)
        
        if opp_data.skills:
            new_opp.skills = self._get_or_create_skills(opp_data.skills)
            
        self.db.add(new_opp)
        self.db.commit()
        self.db.refresh(new_opp)
        return new_opp

    def update(self, opp_id: str, opp_data: OpportunityUpdate):
        opp = self.get_by_id(opp_id)
        if not opp:
            return None
            
        update_data = opp_data.dict(exclude_unset=True)
        skills_data = update_data.pop("skills", None)
        
        for key, value in update_data.items():
            setattr(opp, key, value)
            
        if skills_data is not None:
            opp.skills = self._get_or_create_skills(skills_data)
            
        self.db.commit()
        self.db.refresh(opp)
        return opp

    def delete(self, opp_id: str):
        opp = self.get_by_id(opp_id)
        if opp:
            self.db.delete(opp)
            self.db.commit()
            return True
        return False
