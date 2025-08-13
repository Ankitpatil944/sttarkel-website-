"""
Common Pydantic schemas used across multiple modules.
Provides shared data structures and validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class AssessmentType(str, Enum):
    """Enumeration for assessment types."""
    MCQ = "mcq"
    CODING = "coding"
    APTITUDE = "aptitude"
    INTERVIEW = "interview"


class DifficultyLevel(str, Enum):
    """Enumeration for difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ExperienceLevel(str, Enum):
    """Enumeration for experience levels."""
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"


class Status(str, Enum):
    """Enumeration for status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    skip: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(100, ge=1, le=1000, description="Number of items to return")


class PaginatedResponse(BaseModel):
    """Schema for paginated response."""
    items: List[Any]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str
    detail: Optional[str] = None
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SuccessResponse(BaseModel):
    """Schema for success responses."""
    message: str
    data: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthCheck(BaseModel):
    """Schema for health check response."""
    status: str
    timestamp: datetime
    version: str
    services: Dict[str, str] 