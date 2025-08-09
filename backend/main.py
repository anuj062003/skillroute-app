# backend/main.py
from contextlib import asynccontextmanager
from typing import List, Set
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session, select
from database import create_db_and_tables, engine
from models import Job, Skill
from logic import fetch_jobs_for_role, extract_skills_for_role

class RoadmapRequest(BaseModel):
    current_skills: List[str]
    target_role: str

class RoadmapResponse(BaseModel):
    required_skills: List[str]
    missing_skills: List[str]

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting up...")
    create_db_and_tables()
    yield
    print("Server is shutting down...")

app = FastAPI(lifespan=lifespan)

# --- THIS IS THE PART TO UPDATE ---
# We add your new Vercel URL to the list of allowed origins
origins = [
    "http://localhost:3000",
    "https://skillroute-9abzbvnxx-anujs-projects-358eb027.vercel.app" # Your Vercel Frontend URL
]
# --- END OF UPDATE ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/roadmap", response_model=RoadmapResponse)
def get_roadmap(request: RoadmapRequest, session: Session = Depends(get_session)):
    statement = select(Job).where(Job.title.like(f"%{request.target_role}%"))
    existing_jobs = session.exec(statement).first()

    if not existing_jobs:
        try:
            fetch_jobs_for_role(session, request.target_role)
            extract_skills_for_role(session, request.target_role)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process new role: {e}")

    statement = select(Skill).join(Job.skills).where(Job.title.like(f"%{request.target_role}%"))
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(
            status_code=404, 
            detail=f"Could not extract any known skills for '{request.target_role}'. The job descriptions might be too generic. Try a broader search term like 'Frontend Developer'."
        )
        
    required_skills_set: Set[str] = {skill.name for skill in results}
    current_skills_set: Set[str] = set(skill.lower() for skill in request.current_skills)
    missing_skills_set: Set[str] = required_skills_set - current_skills_set

    return RoadmapResponse(
        required_skills=sorted(list(required_skills_set)),
        missing_skills=sorted(list(missing_skills_set))
    )