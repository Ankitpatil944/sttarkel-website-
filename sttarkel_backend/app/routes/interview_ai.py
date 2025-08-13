"""
AI Interview routes for SttarkelTool backend.
Handles Tavus CVI session creation, management, and feedback.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.db.crud_assessment import (
    create_interview_session, get_interview_session, get_user_interview_sessions,
    update_interview_session, complete_interview_session, delete_interview_session
)
from app.schemas.interview import (
    TavusPersona, InterviewRequest, InterviewSessionResponse, InterviewSessionList,
    InterviewFeedback, TavusSessionRequest, TavusSessionResponse
)
from app.services.ai_interview import ai_interview_service
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/personas", response_model=List[TavusPersona])
async def get_available_personas():
    """Get list of available Tavus personas for interviews."""
    try:
        personas = await ai_interview_service.get_available_personas()
        return personas
        
    except Exception as e:
        logger.error(f"Error getting personas: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get personas")


@router.post("/session", response_model=InterviewSessionResponse)
async def create_interview_session_route(
    request: InterviewRequest,
    db: Session = Depends(get_db)
):
    """Create a new AI interview session."""
    try:
        logger.info(f"Creating interview session for user {request.user_id} with persona {request.persona_id}")
        
        # Get persona details
        persona = await ai_interview_service.get_persona_by_id(request.persona_id)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        
        # Create Tavus session request
        tavus_request = TavusSessionRequest(
            persona_id=request.persona_id,
            user_name=f"User_{request.user_id}",  # In a real app, get actual user name
            user_email=f"user{request.user_id}@example.com",  # In a real app, get actual email
            session_duration=request.session_duration,
            custom_questions=request.custom_questions
        )
        
        # Create Tavus session
        tavus_session = await ai_interview_service.create_interview_session(tavus_request)
        
        # Create database session record
        session_data = {
            "user_id": request.user_id,
            "assessment_id": request.assessment_id,
            "tavus_session_id": tavus_session.session_id,
            "persona_id": request.persona_id,
            "persona_name": persona.name
        }
        
        db_session = create_interview_session(db, session_data)
        
        return InterviewSessionResponse(
            id=db_session.id,
            user_id=db_session.user_id,
            assessment_id=db_session.assessment_id,
            tavus_session_id=db_session.tavus_session_id,
            persona_id=db_session.persona_id,
            persona_name=db_session.persona_name,
            questions_asked=db_session.questions_asked,
            user_responses=db_session.user_responses,
            transcript=db_session.transcript,
            communication_score=db_session.communication_score,
            technical_score=db_session.technical_score,
            confidence_score=db_session.confidence_score,
            overall_score=db_session.overall_score,
            feedback=db_session.feedback,
            strengths=db_session.strengths,
            areas_for_improvement=db_session.areas_for_improvement,
            started_at=db_session.started_at,
            ended_at=db_session.ended_at,
            duration=db_session.duration,
            created_at=db_session.created_at,
            status=db_session.status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating interview session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create interview session")


@router.get("/session/{session_id}", response_model=InterviewSessionResponse)
async def get_interview_session_route(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Get interview session details."""
    try:
        session = get_interview_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Interview session not found")
        
        return InterviewSessionResponse(
            id=session.id,
            user_id=session.user_id,
            assessment_id=session.assessment_id,
            tavus_session_id=session.tavus_session_id,
            persona_id=session.persona_id,
            persona_name=session.persona_name,
            questions_asked=session.questions_asked,
            user_responses=session.user_responses,
            transcript=session.transcript,
            communication_score=session.communication_score,
            technical_score=session.technical_score,
            confidence_score=session.confidence_score,
            overall_score=session.overall_score,
            feedback=session.feedback,
            strengths=session.strengths,
            areas_for_improvement=session.areas_for_improvement,
            started_at=session.started_at,
            ended_at=session.ended_at,
            duration=session.duration,
            created_at=session.created_at,
            status=session.status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting interview session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get interview session")


@router.get("/session/{session_id}/status")
async def get_session_status_route(session_id: int):
    """Get the status of a Tavus interview session."""
    try:
        session = get_interview_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Interview session not found")
        
        if not session.tavus_session_id:
            raise HTTPException(status_code=400, detail="No Tavus session ID found")
        
        status = await ai_interview_service.get_session_status(session.tavus_session_id)
        return status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get session status")


@router.get("/session/{session_id}/transcript")
async def get_session_transcript_route(session_id: int):
    """Get the transcript of an interview session."""
    try:
        session = get_interview_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Interview session not found")
        
        if not session.tavus_session_id:
            raise HTTPException(status_code=400, detail="No Tavus session ID found")
        
        transcript = await ai_interview_service.get_session_transcript(session.tavus_session_id)
        return transcript
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session transcript: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get session transcript")


@router.post("/session/{session_id}/feedback", response_model=InterviewSessionResponse)
async def submit_interview_feedback_route(
    session_id: int,
    feedback: InterviewFeedback,
    db: Session = Depends(get_db)
):
    """Submit feedback for an interview session."""
    try:
        session = get_interview_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Interview session not found")
        
        # Get transcript if not already available
        if not session.transcript and session.tavus_session_id:
            transcript = await ai_interview_service.get_session_transcript(session.tavus_session_id)
            session.transcript = transcript.transcript
        
        # Generate AI feedback if not provided
        if not session.feedback and session.transcript:
            ai_feedback = await ai_interview_service.generate_interview_feedback(transcript)
            feedback.feedback = ai_feedback["feedback"]
            feedback.strengths = ai_feedback["strengths"]
            feedback.areas_for_improvement = ai_feedback["areas_for_improvement"]
        
        # Complete the session
        scores = {
            "communication": feedback.communication_score,
            "technical": feedback.technical_score,
            "confidence": feedback.confidence_score,
            "overall": feedback.overall_score
        }
        
        completed_session = complete_interview_session(
            db, session_id, session.transcript or "", scores, feedback.feedback
        )
        
        return InterviewSessionResponse(
            id=completed_session.id,
            user_id=completed_session.user_id,
            assessment_id=completed_session.assessment_id,
            tavus_session_id=completed_session.tavus_session_id,
            persona_id=completed_session.persona_id,
            persona_name=completed_session.persona_name,
            questions_asked=completed_session.questions_asked,
            user_responses=completed_session.user_responses,
            transcript=completed_session.transcript,
            communication_score=completed_session.communication_score,
            technical_score=completed_session.technical_score,
            confidence_score=completed_session.confidence_score,
            overall_score=completed_session.overall_score,
            feedback=completed_session.feedback,
            strengths=completed_session.strengths,
            areas_for_improvement=completed_session.areas_for_improvement,
            started_at=completed_session.started_at,
            ended_at=completed_session.ended_at,
            duration=completed_session.duration,
            created_at=completed_session.created_at,
            status=completed_session.status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting interview feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit interview feedback")


@router.get("/user/{user_id}/sessions", response_model=InterviewSessionList)
async def get_user_interview_sessions_route(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get interview sessions for a specific user."""
    try:
        sessions = get_user_interview_sessions(db, user_id, skip=skip, limit=limit)
        
        session_responses = []
        for session in sessions:
            session_responses.append(InterviewSessionResponse(
                id=session.id,
                user_id=session.user_id,
                assessment_id=session.assessment_id,
                tavus_session_id=session.tavus_session_id,
                persona_id=session.persona_id,
                persona_name=session.persona_name,
                questions_asked=session.questions_asked,
                user_responses=session.user_responses,
                transcript=session.transcript,
                communication_score=session.communication_score,
                technical_score=session.technical_score,
                confidence_score=session.confidence_score,
                overall_score=session.overall_score,
                feedback=session.feedback,
                strengths=session.strengths,
                areas_for_improvement=session.areas_for_improvement,
                started_at=session.started_at,
                ended_at=session.ended_at,
                duration=session.duration,
                created_at=session.created_at,
                status=session.status
            ))
        
        return InterviewSessionList(
            sessions=session_responses,
            total=len(session_responses),
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting user interview sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user interview sessions")


@router.delete("/session/{session_id}")
async def delete_interview_session_route(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Delete an interview session."""
    try:
        success = delete_interview_session(db, session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Interview session not found")
        
        logger.info(f"Interview session deleted: {session_id}")
        return {"message": "Interview session deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting interview session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete interview session") 