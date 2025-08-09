# backend/api_scraper.py
import os
from serpapi import GoogleSearch
from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import Job

# IMPORTANT: It's best practice to set your API key as an environment variable
# For now, you can paste it here directly for testing.
# To set an environment variable in your terminal (macOS/Linux):
# export SERPAPI_API_KEY="your_api_key_here"
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "fdf52095e691d214549de7e4d8c812fef6f0926ed2e6fbd9816f873b785d8c7f")

def fetch_jobs_from_api(job_title: str):
    """
    Fetches job listings for a given title using the SerpApi Google Jobs API.
    """
    if not SERPAPI_API_KEY or SERPAPI_API_KEY == "PASTE_YOUR_API_KEY_HERE":
        print("🛑 SerpApi API Key not found. Please set the environment variable or paste it in the script.")
        return

    print(f"Fetching jobs for '{job_title}' using SerpApi...")
    params = {
        "api_key": SERPAPI_API_KEY,
        "engine": "google_jobs",
        "q": f"{job_title} India",  # Search query
        "gl": "in",  # Country: India
        "hl": "en",  # Language: English
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "error" in results:
        print(f"API Error: {results['error']}")
        return

    jobs_results = results.get("jobs_results", [])
    print(f"Found {len(jobs_results)} jobs.")

    # Create the database and tables if they don't exist
    create_db_and_tables()

    with Session(engine) as session:
        # Optional: Clear old jobs for this specific title
        statement = select(Job).where(Job.title == job_title)
        existing_jobs = session.exec(statement).all()
        print(f"Deleting {len(existing_jobs)} old jobs for this title.")
        for job in existing_jobs:
            session.delete(job)
        session.commit()

        # Add the new jobs from the API
        print("Adding new jobs to the database...")
        for job_data in jobs_results:
            # We combine the title and company for our main title field, and use the rich description
            full_title = f"{job_data.get('title')} at {job_data.get('company_name')}"
            
            job = Job(
                title=full_title,
                company=job_data.get('company_name'),
                description=job_data.get('description', 'No description available.')
            )
            session.add(job)
        
        session.commit()
    
    print("✅ Done. Database has been updated with new jobs.")


if __name__ == "__main__":
    # You can change this to any role you want to test!
    target_role_to_fetch = "Data Scientist"
    fetch_jobs_from_api(target_role_to_fetch)