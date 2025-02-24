# infrastructure/database.py
import os
from sqlalchemy import create_engine, Column, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment or use a default SQLite URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ingestion_service.db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()


class IngestedDataModel(Base):
    """SQLAlchemy model for ingested data"""
    __tablename__ = "ingested_data"

    id = Column(String, primary_key=True, index=True)
    partner_id = Column(String, index=True)
    payload = Column(JSON)
    timestamp = Column(DateTime)


# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)


# Get a database session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 