"""
Pydantic schemas for Assessment model.
Handles data validation and serialization for assessment operations.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class AssessmentBase(BaseModel):
    """Base assessment schema with common fields."""
    user_id: int = Field(..., description="User ID")
    assessment_type: str = Field(..., description="Type of assessment: mcq, coding, aptitude, interview")
    title: str = Field(..., min_length=1, max_length=200, description="Assessment title")
    description: Optional[str] = Field(None, description="Assessment description")


class AssessmentCreate(AssessmentBase):
    """Schema for creating a new assessment."""
    questions: Optional[Dict[str, Any]] = Field(None, description="Assessment questions")
    correct_answers: Optional[Dict[str, Any]] = Field(None, description="Correct answers")
    max_score: Optional[float] = Field(None, description="Maximum possible score")
    total_questions: Optional[int] = Field(None, description="Total number of questions")


class AssessmentUpdate(BaseModel):
    """Schema for updating assessment information."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    questions: Optional[Dict[str, Any]] = None
    correct_answers: Optional[Dict[str, Any]] = None
    max_score: Optional[float] = None
    total_questions: Optional[int] = None


class AssessmentResponse(AssessmentBase):
    """Schema for assessment response data."""
    id: int
    questions: Optional[Dict[str, Any]] = None
    score: Optional[float] = None
    max_score: Optional[float] = None
    percentage: Optional[float] = None
    time_taken: Optional[int] = None
    total_questions: Optional[int] = None
    correct_count: Optional[int] = None
    feedback: Optional[str] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    recommendations: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    status: str = "pending"
    
    class Config:
        from_attributes = True


class MCQSubmission(BaseModel):
    """Schema for MCQ assessment submission."""
    user_id: int
    answers: Dict[str, str] = Field(..., description="Question ID to answer mapping")
    time_taken: Optional[int] = Field(None, description="Time taken in seconds")


class CodingSubmission(BaseModel):
    """Schema for coding assessment submission."""
    user_id: int
    language: str = Field(..., description="Programming language")
    code: str = Field(..., description="Source code")
    test_cases: Optional[List[Dict[str, Any]]] = Field(None, description="Test cases")
    time_taken: Optional[int] = Field(None, description="Time taken in seconds")


class AptitudeSubmission(BaseModel):
    """Schema for aptitude assessment submission."""
    user_id: int
    answers: Dict[str, str] = Field(..., description="Question ID to answer mapping")
    time_taken: Optional[int] = Field(None, description="Time taken in seconds")


class AssessmentResult(BaseModel):
    """Schema for assessment results."""
    assessment_id: int
    user_id: int
    score: float
    max_score: float
    percentage: float
    correct_count: int
    total_questions: int
    time_taken: int
    feedback: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: str
    completed_at: datetime


class AssessmentList(BaseModel):
    """Schema for list of assessments."""
    assessments: List[AssessmentResponse]
    total: int
    skip: int
    limit: int


# Question schemas
class MCQQuestion(BaseModel):
    """Schema for MCQ question."""
    id: str
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: Optional[str] = Field(None, description="easy, medium, hard")


class CodingQuestion(BaseModel):
    """Schema for coding question."""
    id: str
    title: str
    description: str
    problem_statement: str
    constraints: Optional[str] = None
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None
    test_cases: List[Dict[str, Any]]
    difficulty: Optional[str] = Field(None, description="easy, medium, hard")


class AptitudeQuestion(BaseModel):
    """Schema for aptitude question."""
    id: str
    question: str
    options: List[str]
    correct_answer: str
    category: Optional[str] = Field(None, description="verbal, logical, numerical")
    difficulty: Optional[str] = Field(None, description="easy, medium, hard") 