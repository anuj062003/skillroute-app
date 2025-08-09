# backend/models.py

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

# This is a "Link Table" or "Join Table". It exists to connect one Job to many Skills,
# and one Skill to many Jobs (a many-to-many relationship).
class JobSkillLink(SQLModel, table=True):
    job_id: Optional[int] = Field(default=None, foreign_key="job.id", primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)

# This is our main model for skills
class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True) # Each skill name must be unique

    # The relationship to the Job model, using the link table
    jobs: List["Job"] = Relationship(back_populates="skills", link_model=JobSkillLink)

# This is our main model for jobs
class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    company: Optional[str] = Field(default=None, index=True)
    description: str

    # The relationship to the Skill model, using the link table
    skills: List[Skill] = Relationship(back_populates="jobs", link_model=JobSkillLink)