"""
Pydantic schemas for User model.
Handles data validation and serialization for user operations.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    phone: Optional[str] = Field(None, max_length=20, description="User's phone number")
    experience_level: Optional[str] = Field(None, description="Experience level: junior, mid, senior")
    target_role: Optional[str] = Field(None, max_length=100, description="Target job role")
    target_company: Optional[str] = Field(None, max_length=100, description="Target company")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    experience_level: Optional[str] = None
    target_role: Optional[str] = Field(None, max_length=100)
    target_company: Optional[str] = Field(None, max_length=100)


class UserResponse(UserBase):
    """Schema for user response data."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserStats(BaseModel):
    """Schema for user statistics."""
    user_id: int
    total_assessments: int
    completed_assessments: int
    average_score: float
    best_score: float
    analytics: Optional[dict] = None


class UserList(BaseModel):
    """Schema for list of users."""
    users: list[UserResponse]
    total: int
    skip: int
    limit: int 