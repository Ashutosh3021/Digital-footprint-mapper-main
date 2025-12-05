"""
Database Initialization Script

This script initializes the database tables for the OSINT application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

# Import configuration
from config import Config

def init_database():
    """Initialize the database tables"""
    # Create database engine
    engine = create_engine(Config.DATABASE_URL, echo=True)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()