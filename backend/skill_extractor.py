# backend/skill_extractor.py

from sqlmodel import Session, select

from database import engine
from models import Job, Skill

# This is our "dictionary" of known skills.
# We will search for these keywords in the job descriptions.
SKILLS_LEXICON = [
    'python', 'django', 'flask', 'react', 'vue.js', 'angular',
    'html', 'css', 'javascript', 'typescript',
    'sql', 'postgresql', 'mongodb', 'graphql',
    'aws', 'docker', 'kubernetes', 'git',
    'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch',
    'matplotlib', 'seaborn', 'node.js', 'express.js'
]

def extract_and_save_skills():
    print("Starting skill extraction process...")

    with Session(engine) as session:
        # 1. Fetch all jobs from the database
        statement = select(Job)
        all_jobs = session.exec(statement).all()
        print(f"Found {len(all_jobs)} jobs to process.")

        for job in all_jobs:
            print(f"\nProcessing job: '{job.title}'")
            found_skills_for_job = set()
            description_lower = job.description.lower()

            # 2. Search for each skill from our lexicon in the job description
            for skill_name in SKILLS_LEXICON:
                if skill_name in description_lower:
                    found_skills_for_job.add(skill_name)

            if not found_skills_for_job:
                print(" -> No skills from our lexicon found.")
                continue

            print(f" -> Found skills: {found_skills_for_job}")

            # 3. For each found skill, link it to the current job in the database
            for skill_name in found_skills_for_job:
                # Check if the skill already exists in our 'skill' table
                statement = select(Skill).where(Skill.name == skill_name)
                skill_in_db = session.exec(statement).first()

                if not skill_in_db:
                    # If the skill doesn't exist, create it
                    print(f"    -> New skill '{skill_name}' found, adding to database.")
                    skill_in_db = Skill(name=skill_name)
                    session.add(skill_in_db)

                # Append the skill to the job's list of skills.
                # SQLModel is smart and will automatically create the link
                # in our 'jobskilllink' table.
                if skill_in_db not in job.skills:
                     job.skills.append(skill_in_db)

        # 4. Commit all the changes (new skills and links) to the database
        print("\nCommitting all changes to the database...")
        session.commit()

    print("\nSkill extraction and linking complete! ✅")


if __name__ == "__main__":
    extract_and_save_skills()