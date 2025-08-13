"""
Assessment model for SttarkelTool backend.
Stores assessment results, scores, and performance data.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Assessment(Base):
    """Assessment model for storing assessment results."""
    
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_type = Column(String(50), nullable=False)  # mcq, coding, aptitude, interview
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Assessment data
    questions = Column(JSON, nullable=True)  # Store questions as JSON
    answers = Column(JSON, nullable=True)    # Store user answers as JSON
    correct_answers = Column(JSON, nullable=True)  # Store correct answers as JSON
    
    # Results
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)
    percentage = Column(Float, nullable=True)
    time_taken = Column(Integer, nullable=True)  # in seconds
    total_questions = Column(Integer, nullable=True)
    correct_count = Column(Integer, nullable=True)
    
    # Feedback and analysis
    feedback = Column(Text, nullable=True)
    strengths = Column(JSON, nullable=True)  # List of strengths
    weaknesses = Column(JSON, nullable=True)  # List of areas for improvement
    recommendations = Column(Text, nullable=True)
    
    # Metadata
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Status
    status = Column(String(20), default="pending")  # pending, in_progress, completed, failed
    
    def __repr__(self):
        return f"<Assessment(id={self.id}, type='{self.assessment_type}', score={self.score})>"


class InterviewSession(Base):
    """Interview session model for AI-driven interviews."""
    
    __tablename__ = "interview_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=True)
    
    # Tavus CVI session data
    tavus_session_id = Column(String(100), nullable=True)
    persona_id = Column(String(100), nullable=True)
    persona_name = Column(String(100), nullable=True)
    
    # Session data
    questions_asked = Column(JSON, nullable=True)  # List of questions asked
    user_responses = Column(JSON, nullable=True)   # List of user responses
    transcript = Column(Text, nullable=True)       # Full conversation transcript
    
    # Analysis results
    communication_score = Column(Float, nullable=True)
    technical_score = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)
    
    # Feedback
    feedback = Column(Text, nullable=True)
    strengths = Column(JSON, nullable=True)
    areas_for_improvement = Column(JSON, nullable=True)
    
    # Session metadata
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Integer, nullable=True)  # in seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status
    status = Column(String(20), default="created")  # created, active, completed, failed
    
    def __repr__(self):
        return f"<InterviewSession(id={self.id}, persona='{self.persona_name}', score={self.overall_score})>" 