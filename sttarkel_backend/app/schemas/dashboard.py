"""
Pydantic schemas for Dashboard and Report models.
Handles data validation and serialization for dashboard and reporting operations.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class DashboardBase(BaseModel):
    """Base dashboard schema with common fields."""
    user_id: int = Field(..., description="User ID")


class DashboardResponse(DashboardBase):
    """Schema for dashboard response data."""
    total_assessments: int
    total_interviews: int
    average_assessment_score: float
    average_interview_score: float
    best_assessment_score: float
    best_interview_score: float
    total_time_spent: int  # in seconds
    improvement_rate: Optional[float] = None
    recent_assessments: List[Dict[str, Any]]
    recent_interviews: List[Dict[str, Any]]
    skill_breakdown: Optional[Dict[str, float]] = None
    performance_trend: Optional[List[Dict[str, Any]]] = None


class PerformanceMetrics(BaseModel):
    """Schema for performance metrics."""
    user_id: int
    assessment_metrics: Dict[str, Any]
    interview_metrics: Dict[str, Any]
    overall_metrics: Dict[str, Any]
    skill_analysis: Dict[str, Any]
    recommendations: List[str]


class ReportBase(BaseModel):
    """Base report schema with common fields."""
    user_id: int = Field(..., description="User ID")
    report_type: str = Field(..., description="Type of report: assessment, interview, comprehensive")
    title: str = Field(..., min_length=1, max_length=200, description="Report title")
    description: Optional[str] = Field(None, description="Report description")


class ReportCreate(ReportBase):
    """Schema for creating a new report."""
    assessment_id: Optional[int] = Field(None, description="Associated assessment ID")
    interview_session_id: Optional[int] = Field(None, description="Associated interview session ID")
    content: Optional[Dict[str, Any]] = Field(None, description="Report content data")
    summary: Optional[str] = Field(None, description="Executive summary")
    recommendations: Optional[str] = Field(None, description="Recommendations")


class ReportUpdate(BaseModel):
    """Schema for updating report information."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    recommendations: Optional[str] = None
    status: Optional[str] = None


class ReportResponse(ReportBase):
    """Schema for report response data."""
    id: int
    assessment_id: Optional[int] = None
    interview_session_id: Optional[int] = None
    content: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    recommendations: Optional[str] = None
    overall_score: Optional[float] = None
    mcq_score: Optional[float] = None
    coding_score: Optional[float] = None
    aptitude_score: Optional[float] = None
    interview_score: Optional[float] = None
    pdf_file_path: Optional[str] = None
    pdf_file_size: Optional[int] = None
    performance_breakdown: Optional[Dict[str, Any]] = None
    skill_analysis: Optional[Dict[str, Any]] = None
    improvement_areas: Optional[List[str]] = None
    generated_at: datetime
    expires_at: Optional[datetime] = None
    status: str = "generating"
    
    class Config:
        from_attributes = True


class ReportList(BaseModel):
    """Schema for list of reports."""
    reports: List[ReportResponse]
    total: int
    skip: int
    limit: int


class AnalyticsData(BaseModel):
    """Schema for analytics data."""
    user_id: int
    total_assessments: int
    total_interviews: int
    average_score: float
    best_score: float
    improvement_rate: float
    technical_skills: Dict[str, float]
    soft_skills: Dict[str, float]
    domain_knowledge: Dict[str, float]
    total_time_spent: int
    average_time_per_assessment: float
    fastest_completion: int
    assessment_history: List[Dict[str, Any]]
    interview_history: List[Dict[str, Any]]
    target_score: Optional[float] = None
    target_companies: Optional[List[str]] = None
    target_roles: Optional[List[str]] = None


class SkillAnalysis(BaseModel):
    """Schema for skill analysis."""
    skill_name: str
    current_score: float
    target_score: float
    improvement_needed: float
    recommendations: List[str]
    practice_questions: List[Dict[str, Any]]


class PerformanceTrend(BaseModel):
    """Schema for performance trend data."""
    date: datetime
    assessment_score: Optional[float] = None
    interview_score: Optional[float] = None
    overall_score: Optional[float] = None
    assessment_type: Optional[str] = None


class ReportGenerationRequest(BaseModel):
    """Schema for report generation request."""
    user_id: int
    report_type: str = Field(..., description="assessment, interview, comprehensive")
    assessment_id: Optional[int] = None
    interview_session_id: Optional[int] = None
    include_charts: bool = True
    include_recommendations: bool = True
    format: str = Field("pdf", description="pdf, json")


class ReportDownloadResponse(BaseModel):
    """Schema for report download response."""
    report_id: int
    download_url: str
    file_size: int
    expires_at: datetime
    format: str 