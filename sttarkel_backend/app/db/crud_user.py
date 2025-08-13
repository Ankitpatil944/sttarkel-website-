"""
CRUD operations for User model.
Handles user creation, retrieval, and management.
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import List, Optional


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    db_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        experience_level=user.experience_level,
        target_role=user.target_role,
        target_company=user.target_company
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get list of users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update user information."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def get_user_stats(db: Session, user_id: int) -> dict:
    """Get user statistics and performance metrics."""
    from app.models.assessment import Assessment
    from app.models.report import Analytics
    
    user = get_user(db, user_id)
    if not user:
        return {}
    
    # Get assessment statistics
    assessments = db.query(Assessment).filter(Assessment.user_id == user_id).all()
    total_assessments = len(assessments)
    completed_assessments = len([a for a in assessments if a.status == "completed"])
    
    # Calculate average score
    scores = [a.score for a in assessments if a.score is not None]
    average_score = sum(scores) / len(scores) if scores else 0
    
    # Get analytics
    analytics = db.query(Analytics).filter(Analytics.user_id == user_id).first()
    
    return {
        "user_id": user_id,
        "total_assessments": total_assessments,
        "completed_assessments": completed_assessments,
        "average_score": round(average_score, 2),
        "best_score": max(scores) if scores else 0,
        "analytics": analytics.to_dict() if analytics else None
    } 