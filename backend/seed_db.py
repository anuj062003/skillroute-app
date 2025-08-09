# backend/seed_db.py
from sqlmodel import Session, select
from database import engine, create_db_and_tables # <-- CHANGE 1: Import the create_db_and_tables function
from models import Job

def seed_database():
    print("Seeding database with sample job data...")
    
    # --- CHANGE 2: Call the function to create tables ---
    # This ensures the tables exist before we try to use them.
    create_db_and_tables()

    # A list of sample jobs. We've included rich descriptions with various skills.
    sample_jobs = [
        {
            "title": "Senior Python Developer",
            "company": "Tech Innovators Inc.",
            "description": "We are looking for a Senior Python Developer with over 5 years of experience in building scalable web applications. Must have strong skills in Django, Flask, and REST APIs. Experience with PostgreSQL, Docker, and AWS is a huge plus. Familiarity with React or Vue.js on the frontend is desired."
        },
        {
            "title": "Data Scientist",
            "company": "Data Insights Corp.",
            "description": "Join our data science team! You will be working with large datasets to extract meaningful insights. Required skills include Python, Pandas, NumPy, and Scikit-learn. You must be proficient in SQL. Experience with machine learning frameworks like TensorFlow or PyTorch is highly desirable. Knowledge of data visualization tools like Matplotlib and Seaborn is key."
        },
        {
            "title": "Junior Frontend Developer",
            "company": "Creative Solutions",
            "description": "We have an opening for a Junior Frontend Developer. You will be responsible for building user interfaces for our clients. Must have a solid understanding of HTML, CSS, and JavaScript. Experience with a modern framework like React or Angular is required. Knowledge of Git and RESTful services is important."
        },
        {
            "title": "Full Stack Engineer",
            "company": "Connect All Platforms",
            "description": "Seeking a Full Stack Engineer to work on both our frontend and backend systems. Our stack is Node.js and Express.js on the backend, and React on the frontend. We use MongoDB as our database. Experience with GraphQL, TypeScript, and deploying applications using Docker and Kubernetes is preferred."
        }
    ]
    
    with Session(engine) as session:
        # --- CHANGE 3: Use modern syntax to fix the DeprecationWarning ---
        print("Clearing old job data...")
        # Select all existing job objects
        statement = select(Job)
        existing_jobs = session.exec(statement).all()
        # Delete each one
        for job in existing_jobs:
            session.delete(job)
        session.commit()

        # Add the new sample jobs
        print("Adding new sample jobs...")
        for job_data in sample_jobs:
            job = Job(title=job_data["title"], company=job_data["company"], description=job_data["description"])
            session.add(job)
        
        session.commit()

    print("Database seeding complete! ✅")


if __name__ == "__main__":
    seed_database()