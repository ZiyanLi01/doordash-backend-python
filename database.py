from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variable or default to Supabase
DATABASE_URL = os.getenv(
    "SUPABASE_DB_URL", 
    "postgresql://postgres:3v6-U.sbMnYB%403D@db.fbqinbkfgckofqokgevu.supabase.co:5432/postgres?sslmode=require"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
