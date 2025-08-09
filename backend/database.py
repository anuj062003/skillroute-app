# backend/database.py

from sqlmodel import SQLModel, create_engine

# Define the name of our database file
sqlite_file_name = "database.db"
# Create the connection URL
sqlite_url = f"sqlite:///{sqlite_file_name}"

# The engine is the main object that manages the connection to the database
# connect_args is needed only for SQLite to allow it to be used by multiple threads
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

# This function will be called to create the database and tables
def create_db_and_tables():
    # SQLModel.metadata.create_all() inspects all the classes that inherit
    # from SQLModel and creates the corresponding tables in the database.
    SQLModel.metadata.create_all(engine)