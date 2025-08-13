"""
CRUD operations for Assessment and InterviewSession models.
Handles assessment creation, retrieval, and management.
"""

from sqlalchemy.orm import Session
from app.models.assessment import Assessment, InterviewSession
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate
from app.schemas.interview import InterviewSessionCreate
from typing import List, Optional
from datetime import datetime


# Assessment CRUD operations
def create_assessment(db: Session, assessment: AssessmentCreate) -> Assessment:
    """Create a new assessment."""
    db_assessment = Assessment(
        user_id=assessment.user_id,
        assessment_type=assessment.assessment_type,
        title=assessment.title,
        description=assessment.description,
        questions=assessment.questions,
        correct_answers=assessment.correct_answers,
        max_score=assessment.max_score,
        total_questions=assessment.total_questions,
        started_at=datetime.utcnow()
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


def get_assessment(db: Session, assessment_id: int) -> Optional[Assessment]:
    """Get assessment by ID."""
    return db.query(Assessment).filter(Assessment.id == assessment_id).first()


def get_user_assessments(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Assessment]:
    """Get assessments for a specific user."""
    return db.query(Assessment).filter(Assessment.user_id == user_id).offset(skip).limit(limit).all()


def update_assessment(db: Session, assessment_id: int, assessment_update: AssessmentUpdate) -> Optional[Assessment]:
    """Update assessment information."""
    db_assessment = get_assessment(db, assessment_id)
    if not db_assessment:
        return None
    
    update_data = assessment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_assessment, field, value)
    
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


def complete_assessment(db: Session, assessment_id: int, answers: dict, score: float, feedback: str = None) -> Optional[Assessment]:
    """Complete an assessment with results."""
    db_assessment = get_assessment(db, assessment_id)
    if not db_assessment:
        return None
    
    # Calculate results
    correct_count = 0
    if db_assessment.correct_answers and answers:
        for question_id, user_answer in answers.items():
            if question_id in db_assessment.correct_answers:
                if user_answer == db_assessment.correct_answers[question_id]:
                    correct_count += 1
    
    # Update assessment
    db_assessment.answers = answers
    db_assessment.score = score
    db_assessment.correct_count = correct_count
    db_assessment.percentage = (score / db_assessment.max_score * 100) if db_assessment.max_score else 0
    db_assessment.feedback = feedback
    db_assessment.completed_at = datetime.utcnow()
    db_assessment.status = "completed"
    
    # Calculate time taken
    if db_assessment.started_at:
        time_taken = (db_assessment.completed_at - db_assessment.started_at).total_seconds()
        db_assessment.time_taken = int(time_taken)
    
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


def delete_assessment(db: Session, assessment_id: int) -> bool:
    """Delete an assessment."""
    db_assessment = get_assessment(db, assessment_id)
    if not db_assessment:
        return False
    
    db.delete(db_assessment)
    db.commit()
    return True


# Interview Session CRUD operations
def create_interview_session(db: Session, session: InterviewSessionCreate) -> InterviewSession:
    """Create a new interview session."""
    db_session = InterviewSession(
        user_id=session.user_id,
        assessment_id=session.assessment_id,
        tavus_session_id=session.tavus_session_id,
        persona_id=session.persona_id,
        persona_name=session.persona_name,
        started_at=datetime.utcnow(),
        status="active"
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_interview_session(db: Session, session_id: int) -> Optional[InterviewSession]:
    """Get interview session by ID."""
    return db.query(InterviewSession).filter(InterviewSession.id == session_id).first()


def get_user_interview_sessions(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[InterviewSession]:
    """Get interview sessions for a specific user."""
    return db.query(InterviewSession).filter(InterviewSession.user_id == user_id).offset(skip).limit(limit).all()


def update_interview_session(db: Session, session_id: int, **kwargs) -> Optional[InterviewSession]:
    """Update interview session information."""
    db_session = get_interview_session(db, session_id)
    if not db_session:
        return None
    
    for field, value in kwargs.items():
        if hasattr(db_session, field):
            setattr(db_session, field, value)
    
    db.commit()
    db.refresh(db_session)
    return db_session


def complete_interview_session(db: Session, session_id: int, transcript: str, scores: dict, feedback: str) -> Optional[InterviewSession]:
    """Complete an interview session with results."""
    db_session = get_interview_session(db, session_id)
    if not db_session:
        return None
    
    # Update session with results
    db_session.transcript = transcript
    db_session.communication_score = scores.get("communication", 0)
    db_session.technical_score = scores.get("technical", 0)
    db_session.confidence_score = scores.get("confidence", 0)
    db_session.overall_score = scores.get("overall", 0)
    db_session.feedback = feedback
    db_session.ended_at = datetime.utcnow()
    db_session.status = "completed"
    
    # Calculate duration
    if db_session.started_at and db_session.ended_at:
        duration = (db_session.ended_at - db_session.started_at).total_seconds()
        db_session.duration = int(duration)
    
    db.commit()
    db.refresh(db_session)
    return db_session


def delete_interview_session(db: Session, session_id: int) -> bool:
    """Delete an interview session."""
    db_session = get_interview_session(db, session_id)
    if not db_session:
        return False
    
    db.delete(db_session)
    db.commit()
    return True


# Analytics functions
def get_user_performance_summary(db: Session, user_id: int) -> dict:
    """Get comprehensive performance summary for a user."""
    assessments = get_user_assessments(db, user_id)
    interview_sessions = get_user_interview_sessions(db, user_id)
    
    # Calculate assessment statistics
    assessment_scores = [a.score for a in assessments if a.score is not None]
    avg_assessment_score = sum(assessment_scores) / len(assessment_scores) if assessment_scores else 0
    
    # Calculate interview statistics
    interview_scores = [s.overall_score for s in interview_sessions if s.overall_score is not None]
    avg_interview_score = sum(interview_scores) / len(interview_scores) if interview_scores else 0
    
    return {
        "user_id": user_id,
        "total_assessments": len(assessments),
        "total_interviews": len(interview_sessions),
        "average_assessment_score": round(avg_assessment_score, 2),
        "average_interview_score": round(avg_interview_score, 2),
        "best_assessment_score": max(assessment_scores) if assessment_scores else 0,
        "best_interview_score": max(interview_scores) if interview_scores else 0,
        "recent_assessments": [a.to_dict() for a in assessments[-5:]],  # Last 5 assessments
        "recent_interviews": [s.to_dict() for s in interview_sessions[-5:]]  # Last 5 interviews
    } 