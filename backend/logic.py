import os
from serpapi import GoogleSearch
from sqlmodel import Session, select
from models import Job, Skill

# --- SKILL EXTRACTOR LOGIC ---
SKILLS_LEXICON = [
    # Frontend
    'react', 'vue.js', 'vue', 'angular', 'next.js', 'svelte', 'html', 'css', 
    'javascript', 'typescript', 'redux', 'webpack', 'babel', 'jest', 
    'vite', 'tailwind', 'sass', 'bootstrap',
    
    # Backend
    'python', 'django', 'flask', 'node.js', 'express.js', 'java', 'spring boot',
    'c#', '.net', 'swift', 'kotlin', 'php', 'laravel', 'ruby', 'ruby on rails',
    'rust', 'go', 'golang',
    
    # Database
    'sql', 'postgresql', 'mongodb', 'graphql', 'mysql', 'nosql', 'redis', 'firebase',
    
    # DevOps & Cloud
    'aws', 'docker', 'kubernetes', 'git', 'azure', 'gcp', 'terraform',
    'ci/cd', 'jenkins', 'ansible', 'nginx',
    
    # Data Science & ML
    'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch',
    'matplotlib', 'seaborn', 'mlops', 'jupyter'
]

def extract_skills_for_role(session: Session, job_title: str):
    print(f"Extracting skills for all '{job_title}' jobs...")
    statement = select(Job).where(Job.title.like(f"%{job_title}%"))
    jobs_to_process = session.exec(statement).all()

    total_skills_linked = 0
    for job in jobs_to_process:
        found_skills_for_job = set()
        description_lower = job.description.lower()
        # Simple word boundary check to avoid matching substrings
        for skill_name in SKILLS_LEXICON:
            if f' {skill_name} ' in f' {description_lower} ':
                found_skills_for_job.add(skill_name)
        
        if not found_skills_for_job:
            continue

        for skill_name in found_skills_for_job:
            statement = select(Skill).where(Skill.name == skill_name)
            skill_in_db = session.exec(statement).first()
            if not skill_in_db:
                skill_in_db = Skill(name=skill_name)
                session.add(skill_in_db)
            if skill_in_db not in job.skills:
                job.skills.append(skill_in_db)
                total_skills_linked += 1
    
    session.commit()
    print(f"Skill extraction complete. Linked {total_skills_linked} new skills.")


# --- API SCRAPER LOGIC ---
def fetch_jobs_for_role(session: Session, job_title: str):
    # Read the API key from the environment variables
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    
    if not SERPAPI_API_KEY:
        print("🛑 SerpApi API Key not found in environment variables.")
        raise Exception("SerpApi API Key not configured.")
    
    print(f"Fetching live job data for '{job_title}' from SerpApi...")
    params = {
        "api_key": SERPAPI_API_KEY,
        "engine": "google_jobs",
        "q": f"{job_title} India",
        "gl": "in",
        "hl": "en",
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if "error" in results:
        raise Exception(f"API Error: {results['error']}")

    jobs_results = results.get("jobs_results", [])
    print(f"Found {len(jobs_results)} jobs.")
    
    for job_data in jobs_results:
        full_title = f"{job_data.get('title')} at {job_data.get('company_name')}"
        job = Job(
            title=full_title,
            company=job_data.get('company_name'),
            description=job_data.get('description', 'No description available.')
        )
        session.add(job)
    
    session.commit()
    print("New jobs added to database.")