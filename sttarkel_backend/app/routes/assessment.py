"""
Assessment routes for SttarkelTool backend.
Handles MCQ, coding, and aptitude assessment endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.db.crud_assessment import (
    create_assessment, get_assessment, get_user_assessments,
    complete_assessment, delete_assessment
)
from app.schemas.assessment import (
    AssessmentCreate, AssessmentResponse, AssessmentList,
    MCQSubmission, CodingSubmission, AptitudeSubmission,
    AssessmentResult, MCQQuestion, CodingQuestion, AptitudeQuestion
)
from app.services.mcq_service import mcq_service
from app.services.coding_service import coding_service
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/mcq", response_model=AssessmentResult)
async def submit_mcq_assessment(
    submission: MCQSubmission,
    db: Session = Depends(get_db)
):
    """Submit MCQ assessment answers and get results."""
    try:
        logger.info(f"Processing MCQ submission for user {submission.user_id}")
        
        # Get assessment data
        assessment_data = await mcq_service.generate_mcq_assessment(
            category="programming",
            difficulty="medium",
            count=5
        )
        
        # Evaluate submission
        result = await mcq_service.evaluate_mcq_submission(
            submission, assessment_data["correct_answers"]
        )
        
        # Create assessment record
        assessment = AssessmentCreate(
            user_id=submission.user_id,
            assessment_type="mcq",
            title="Programming MCQ Assessment",
            description="Multiple choice questions on programming concepts",
            questions=assessment_data["questions"],
            correct_answers=assessment_data["correct_answers"],
            max_score=assessment_data["max_score"],
            total_questions=assessment_data["total_questions"]
        )
        
        db_assessment = create_assessment(db, assessment)
        
        # Complete assessment with results
        complete_assessment(
            db, db_assessment.id, submission.answers, result["score"], result["feedback"]
        )
        
        return AssessmentResult(
            assessment_id=db_assessment.id,
            user_id=submission.user_id,
            score=result["score"],
            max_score=result["max_score"],
            percentage=result["percentage"],
            correct_count=result["correct_count"],
            total_questions=result["total_questions"],
            time_taken=result["time_taken"],
            feedback=result["feedback"],
            strengths=result["strengths"],
            weaknesses=result["weaknesses"],
            recommendations=result["recommendations"],
            completed_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error processing MCQ submission: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process MCQ assessment")


@router.post("/coding", response_model=AssessmentResult)
async def submit_coding_assessment(
    submission: CodingSubmission,
    db: Session = Depends(get_db)
):
    """Submit coding assessment and get results."""
    try:
        logger.info(f"Processing coding submission for user {submission.user_id}")
        
        # Get coding question
        question_data = await coding_service.generate_coding_assessment(
            difficulty="medium",
            language=submission.language
        )
        
        question = CodingQuestion(**question_data["question"])
        
        # Evaluate submission
        result = await coding_service.evaluate_coding_submission(submission, question)
        
        # Create assessment record
        assessment = AssessmentCreate(
            user_id=submission.user_id,
            assessment_type="coding",
            title=f"Coding Assessment - {question.title}",
            description=question.description,
            questions={"question": question.dict()},
            max_score=100,
            total_questions=1
        )
        
        db_assessment = create_assessment(db, assessment)
        
        # Complete assessment with results
        complete_assessment(
            db, db_assessment.id, {"code": submission.code}, result["score"], result["feedback"]
        )
        
        return AssessmentResult(
            assessment_id=db_assessment.id,
            user_id=submission.user_id,
            score=result["score"],
            max_score=result["max_score"],
            percentage=result["percentage"],
            correct_count=result["passed_tests"],
            total_questions=result["total_tests"],
            time_taken=result["time_taken"],
            feedback=result["feedback"],
            strengths=result["strengths"],
            weaknesses=result["weaknesses"],
            recommendations=result["recommendations"],
            completed_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error processing coding submission: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process coding assessment")


@router.get("/user/{user_id}", response_model=AssessmentList)
async def get_user_assessments_route(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    assessment_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get assessments for a specific user."""
    try:
        assessments = get_user_assessments(db, user_id, skip=skip, limit=limit)
        
        if assessment_type:
            assessments = [a for a in assessments if a.assessment_type == assessment_type]
        
        assessment_responses = []
        for assessment in assessments:
            assessment_responses.append(AssessmentResponse(
                id=assessment.id,
                user_id=assessment.user_id,
                assessment_type=assessment.assessment_type,
                title=assessment.title,
                description=assessment.description,
                questions=assessment.questions,
                score=assessment.score,
                max_score=assessment.max_score,
                percentage=assessment.percentage,
                time_taken=assessment.time_taken,
                total_questions=assessment.total_questions,
                correct_count=assessment.correct_count,
                feedback=assessment.feedback,
                strengths=assessment.strengths,
                weaknesses=assessment.weaknesses,
                recommendations=assessment.recommendations,
                started_at=assessment.started_at,
                completed_at=assessment.completed_at,
                created_at=assessment.created_at,
                updated_at=assessment.updated_at,
                status=assessment.status
            ))
        
        return AssessmentList(
            assessments=assessment_responses,
            total=len(assessment_responses),
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting user assessments: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user assessments")


@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment_route(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific assessment by ID."""
    try:
        assessment = get_assessment(db, assessment_id)
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        return AssessmentResponse(
            id=assessment.id,
            user_id=assessment.user_id,
            assessment_type=assessment.assessment_type,
            title=assessment.title,
            description=assessment.description,
            questions=assessment.questions,
            score=assessment.score,
            max_score=assessment.max_score,
            percentage=assessment.percentage,
            time_taken=assessment.time_taken,
            total_questions=assessment.total_questions,
            correct_count=assessment.correct_count,
            feedback=assessment.feedback,
            strengths=assessment.strengths,
            weaknesses=assessment.weaknesses,
            recommendations=assessment.recommendations,
            started_at=assessment.started_at,
            completed_at=assessment.completed_at,
            created_at=assessment.created_at,
            updated_at=assessment.updated_at,
            status=assessment.status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting assessment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get assessment") 