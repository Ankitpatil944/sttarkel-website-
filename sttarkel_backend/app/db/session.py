"""
Database session configuration for SttarkelTool backend.
Handles SQLAlchemy session creation and database initialization.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
import asyncio

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=settings.debug
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database tables."""
    # Import all models to ensure they are registered
    from app.models.user import User
    from app.models.assessment import Assessment, InterviewSession
    from app.models.report import Report, Analytics
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def get_db_session() -> Session:
    """Get a database session for synchronous operations."""
    return SessionLocal() 