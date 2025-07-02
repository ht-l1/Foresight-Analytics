# setting up SQLAlchemy (ORM) to connect to the database

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Neon URL, fall bac can you explai the relationship k to local PostgreSQL
database_url = settings.neon_database_url or settings.database_url

engine = create_engine(database_url)
SessionLocal = sessionmaker(automcommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()