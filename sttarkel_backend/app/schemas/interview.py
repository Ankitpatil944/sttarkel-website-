"""
Pydantic schemas for Interview model.
Handles data validation and serialization for interview operations.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class InterviewSessionBase(BaseModel):
    """Base interview session schema with common fields."""
    user_id: int = Field(..., description="User ID")
    assessment_id: Optional[int] = Field(None, description="Associated assessment ID")


class InterviewSessionCreate(InterviewSessionBase):
    """Schema for creating a new interview session."""
    tavus_session_id: Optional[str] = Field(None, description="Tavus CVI session ID")
    persona_id: Optional[str] = Field(None, description="Tavus persona ID")
    persona_name: Optional[str] = Field(None, description="Tavus persona name")


class InterviewSessionUpdate(BaseModel):
    """Schema for updating interview session information."""
    tavus_session_id: Optional[str] = None
    persona_id: Optional[str] = None
    persona_name: Optional[str] = None
    questions_asked: Optional[List[str]] = None
    user_responses: Optional[List[str]] = None
    transcript: Optional[str] = None
    communication_score: Optional[float] = None
    technical_score: Optional[float] = None
    confidence_score: Optional[float] = None
    overall_score: Optional[float] = None
    feedback: Optional[str] = None
    strengths: Optional[List[str]] = None
    areas_for_improvement: Optional[List[str]] = None
    status: Optional[str] = None


class InterviewSessionResponse(InterviewSessionBase):
    """Schema for interview session response data."""
    id: int
    tavus_session_id: Optional[str] = None
    persona_id: Optional[str] = None
    persona_name: Optional[str] = None
    questions_asked: Optional[List[str]] = None
    user_responses: Optional[List[str]] = None
    transcript: Optional[str] = None
    communication_score: Optional[float] = None
    technical_score: Optional[float] = None
    confidence_score: Optional[float] = None
    overall_score: Optional[float] = None
    feedback: Optional[str] = None
    strengths: Optional[List[str]] = None
    areas_for_improvement: Optional[List[str]] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration: Optional[int] = None
    created_at: datetime
    status: str = "created"
    
    class Config:
        from_attributes = True


class TavusPersona(BaseModel):
    """Schema for Tavus persona information."""
    id: str
    name: str
    description: str
    role: str
    company: Optional[str] = None
    industry: Optional[str] = None
    difficulty: Optional[str] = Field(None, description="easy, medium, hard")
    specialties: Optional[List[str]] = None
    avatar_url: Optional[str] = None


class InterviewRequest(BaseModel):
    """Schema for interview session request."""
    user_id: int
    persona_id: str = Field(..., description="Tavus persona ID")
    assessment_id: Optional[int] = None
    custom_questions: Optional[List[str]] = None
    session_duration: Optional[int] = Field(1800, description="Session duration in seconds")


class InterviewFeedback(BaseModel):
    """Schema for interview feedback."""
    session_id: int
    communication_score: float = Field(..., ge=0, le=100, description="Communication score (0-100)")
    technical_score: float = Field(..., ge=0, le=100, description="Technical score (0-100)")
    confidence_score: float = Field(..., ge=0, le=100, description="Confidence score (0-100)")
    overall_score: float = Field(..., ge=0, le=100, description="Overall score (0-100)")
    feedback: str = Field(..., description="Detailed feedback")
    strengths: List[str] = Field(..., description="List of strengths")
    areas_for_improvement: List[str] = Field(..., description="Areas for improvement")
    transcript: Optional[str] = Field(None, description="Full conversation transcript")


class InterviewSessionList(BaseModel):
    """Schema for list of interview sessions."""
    sessions: List[InterviewSessionResponse]
    total: int
    skip: int
    limit: int


class InterviewAnalytics(BaseModel):
    """Schema for interview analytics."""
    total_sessions: int
    average_communication_score: float
    average_technical_score: float
    average_confidence_score: float
    average_overall_score: float
    best_overall_score: float
    total_duration: int  # in seconds
    average_duration: float  # in seconds
    sessions_by_persona: Dict[str, int]
    recent_sessions: List[InterviewSessionResponse]


# Tavus API schemas
class TavusSessionRequest(BaseModel):
    """Schema for Tavus CVI session creation request."""
    persona_id: str
    user_name: str
    user_email: str
    session_duration: Optional[int] = 1800
    custom_questions: Optional[List[str]] = None


class TavusSessionResponse(BaseModel):
    """Schema for Tavus CVI session response."""
    session_id: str
    session_url: str
    status: str
    created_at: datetime
    expires_at: Optional[datetime] = None


class TavusTranscript(BaseModel):
    """Schema for Tavus interview transcript."""
    session_id: str
    transcript: str
    duration: int
    questions_asked: List[str]
    user_responses: List[str]
    analysis: Optional[Dict[str, Any]] = None 