"""
Report model for SttarkelTool backend.
Stores generated PDF reports and analytics data.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, JSON, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class Report(Base):
    """Report model for storing generated PDF reports."""
    
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=True)
    interview_session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=True)
    
    # Report metadata
    report_type = Column(String(50), nullable=False)  # assessment, interview, comprehensive
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Report content
    content = Column(JSON, nullable=True)  # Structured report data
    summary = Column(Text, nullable=True)  # Executive summary
    recommendations = Column(Text, nullable=True)
    
    # Performance metrics
    overall_score = Column(Float, nullable=True)
    mcq_score = Column(Float, nullable=True)
    coding_score = Column(Float, nullable=True)
    aptitude_score = Column(Float, nullable=True)
    interview_score = Column(Float, nullable=True)
    
    # PDF file
    pdf_file_path = Column(String(500), nullable=True)
    pdf_file_size = Column(Integer, nullable=True)
    
    # Analytics data
    performance_breakdown = Column(JSON, nullable=True)  # Detailed performance metrics
    skill_analysis = Column(JSON, nullable=True)  # Skill-wise analysis
    improvement_areas = Column(JSON, nullable=True)  # Areas for improvement
    
    # Metadata
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    status = Column(String(20), default="generating")  # generating, completed, failed
    
    def __repr__(self):
        return f"<Report(id={self.id}, type='{self.report_type}', score={self.overall_score})>"


class Analytics(Base):
    """Analytics model for storing user performance analytics."""
    
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Performance metrics
    total_assessments = Column(Integer, default=0)
    total_interviews = Column(Integer, default=0)
    average_score = Column(Float, nullable=True)
    best_score = Column(Float, nullable=True)
    improvement_rate = Column(Float, nullable=True)
    
    # Skill metrics
    technical_skills = Column(JSON, nullable=True)  # Skill-wise scores
    soft_skills = Column(JSON, nullable=True)       # Communication, leadership, etc.
    domain_knowledge = Column(JSON, nullable=True)  # Industry-specific knowledge
    
    # Time-based metrics
    total_time_spent = Column(Integer, default=0)  # Total time in seconds
    average_time_per_assessment = Column(Float, nullable=True)
    fastest_completion = Column(Integer, nullable=True)  # in seconds
    
    # Progress tracking
    assessment_history = Column(JSON, nullable=True)  # List of assessment IDs with scores
    interview_history = Column(JSON, nullable=True)   # List of interview session IDs with scores
    
    # Goals and targets
    target_score = Column(Float, nullable=True)
    target_companies = Column(JSON, nullable=True)  # List of target companies
    target_roles = Column(JSON, nullable=True)      # List of target roles
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Analytics(user_id={self.user_id}, avg_score={self.average_score})>" 