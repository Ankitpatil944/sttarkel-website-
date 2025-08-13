"""
Authentication routes for SttarkelTool backend.
Simple user management without JWT tokens.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.db.crud_user import (
    create_user, get_user, get_user_by_email, get_users,
    update_user, delete_user, get_user_stats
)
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserStats, UserList
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    try:
        # Check if user already exists
        existing_user = get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Create new user
        db_user = create_user(db, user)
        
        logger.info(f"New user registered: {db_user.email}")
        return UserResponse(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            phone=db_user.phone,
            experience_level=db_user.experience_level,
            target_role=db_user.target_role,
            target_company=db_user.target_company,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to register user")


@router.get("/users", response_model=UserList)
async def get_users_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get list of users with pagination."""
    try:
        users = get_users(db, skip=skip, limit=limit)
        
        user_responses = []
        for user in users:
            user_responses.append(UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                phone=user.phone,
                experience_level=user.experience_level,
                target_role=user.target_role,
                target_company=user.target_company,
                created_at=user.created_at,
                updated_at=user.updated_at
            ))
        
        return UserList(
            users=user_responses,
            total=len(user_responses),
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get users")


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_route(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific user by ID."""
    try:
        user = get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            experience_level=user.experience_level,
            target_role=user.target_role,
            target_company=user.target_company,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user")


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_route(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update user information."""
    try:
        updated_user = update_user(db, user_id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        logger.info(f"User updated: {updated_user.email}")
        return UserResponse(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            phone=updated_user.phone,
            experience_level=updated_user.experience_level,
            target_role=updated_user.target_role,
            target_company=updated_user.target_company,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update user")


@router.delete("/users/{user_id}")
async def delete_user_route(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a user."""
    try:
        success = delete_user(db, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        
        logger.info(f"User deleted: {user_id}")
        return {"message": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete user")


@router.get("/users/{user_id}/stats", response_model=UserStats)
async def get_user_stats_route(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user statistics and performance metrics."""
    try:
        stats = get_user_stats(db, user_id)
        if not stats:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserStats(**stats)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user stats")


@router.get("/profile/{user_id}", response_model=UserResponse)
async def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user profile information."""
    try:
        user = get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            experience_level=user.experience_level,
            target_role=user.target_role,
            target_company=user.target_company,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user profile") 