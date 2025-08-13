"""
Dashboard routes for SttarkelTool backend.
Handles analytics, performance tracking, and report generation.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.db.crud_assessment import get_user_performance_summary
from app.schemas.dashboard import (
    DashboardResponse, PerformanceMetrics, ReportResponse, ReportList,
    AnalyticsData, ReportGenerationRequest
)
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/user/{user_id}", response_model=DashboardResponse)
async def get_user_dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard data for a user."""
    try:
        # Get performance summary
        performance_summary = get_user_performance_summary(db, user_id)
        
        if not performance_summary:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Calculate additional metrics
        total_assessments = performance_summary.get("total_assessments", 0)
        total_interviews = performance_summary.get("total_interviews", 0)
        avg_assessment_score = performance_summary.get("average_assessment_score", 0)
        avg_interview_score = performance_summary.get("average_interview_score", 0)
        best_assessment_score = performance_summary.get("best_assessment_score", 0)
        best_interview_score = performance_summary.get("best_interview_score", 0)
        
        # Mock data for demonstration
        total_time_spent = 3600  # 1 hour in seconds
        improvement_rate = 15.5  # 15.5% improvement
        
        # Recent assessments and interviews
        recent_assessments = performance_summary.get("recent_assessments", [])
        recent_interviews = performance_summary.get("recent_interviews", [])
        
        # Skill breakdown (mock data)
        skill_breakdown = {
            "programming": 75.0,
            "problem_solving": 68.0,
            "communication": 82.0,
            "aptitude": 71.0
        }
        
        # Performance trend (mock data)
        performance_trend = [
            {"date": "2024-01-01", "score": 65, "type": "assessment"},
            {"date": "2024-01-05", "score": 72, "type": "assessment"},
            {"date": "2024-01-10", "score": 78, "type": "interview"},
            {"date": "2024-01-15", "score": 85, "type": "assessment"}
        ]
        
        return DashboardResponse(
            user_id=user_id,
            total_assessments=total_assessments,
            total_interviews=total_interviews,
            average_assessment_score=avg_assessment_score,
            average_interview_score=avg_interview_score,
            best_assessment_score=best_assessment_score,
            best_interview_score=best_interview_score,
            total_time_spent=total_time_spent,
            improvement_rate=improvement_rate,
            recent_assessments=recent_assessments,
            recent_interviews=recent_interviews,
            skill_breakdown=skill_breakdown,
            performance_trend=performance_trend
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user dashboard")


@router.get("/analytics/{user_id}", response_model=AnalyticsData)
async def get_user_analytics(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed analytics for a user."""
    try:
        # Get performance summary
        performance_summary = get_user_performance_summary(db, user_id)
        
        if not performance_summary:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Mock analytics data
        analytics_data = {
            "user_id": user_id,
            "total_assessments": performance_summary.get("total_assessments", 0),
            "total_interviews": performance_summary.get("total_interviews", 0),
            "average_score": performance_summary.get("average_assessment_score", 0),
            "best_score": performance_summary.get("best_assessment_score", 0),
            "improvement_rate": 15.5,
            "technical_skills": {
                "programming": 75.0,
                "algorithms": 68.0,
                "data_structures": 72.0,
                "system_design": 65.0
            },
            "soft_skills": {
                "communication": 82.0,
                "leadership": 70.0,
                "teamwork": 78.0,
                "problem_solving": 75.0
            },
            "domain_knowledge": {
                "web_development": 80.0,
                "mobile_development": 65.0,
                "cloud_computing": 70.0,
                "machine_learning": 60.0
            },
            "total_time_spent": 3600,
            "average_time_per_assessment": 1800,
            "fastest_completion": 900,
            "assessment_history": performance_summary.get("recent_assessments", []),
            "interview_history": performance_summary.get("recent_interviews", []),
            "target_score": 85.0,
            "target_companies": ["Google", "Microsoft", "Amazon", "Meta"],
            "target_roles": ["Software Engineer", "Senior Developer", "Tech Lead"]
        }
        
        return AnalyticsData(**analytics_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user analytics")


@router.post("/report/generate", response_model=ReportResponse)
async def generate_report(
    request: ReportGenerationRequest,
    db: Session = Depends(get_db)
):
    """Generate a comprehensive report for a user."""
    try:
        # Mock report generation
        report_data = {
            "id": 1,  # In real app, this would be generated
            "user_id": request.user_id,
            "report_type": request.report_type,
            "title": f"{request.report_type.title()} Report for User {request.user_id}",
            "description": f"Comprehensive {request.report_type} analysis and recommendations",
            "content": {
                "summary": "User shows strong potential with areas for improvement",
                "performance_metrics": {
                    "overall_score": 75.5,
                    "assessment_score": 78.0,
                    "interview_score": 72.0
                },
                "skill_analysis": {
                    "strengths": ["Problem solving", "Technical knowledge"],
                    "weaknesses": ["Communication", "Time management"]
                }
            },
            "summary": "User demonstrates solid technical foundation with room for improvement in soft skills.",
            "recommendations": "Focus on communication skills and practice mock interviews regularly.",
            "overall_score": 75.5,
            "mcq_score": 80.0,
            "coding_score": 75.0,
            "aptitude_score": 70.0,
            "interview_score": 72.0,
            "pdf_file_path": f"/reports/user_{request.user_id}_{request.report_type}.pdf",
            "pdf_file_size": 1024000,
            "performance_breakdown": {
                "technical": 78.0,
                "communication": 65.0,
                "problem_solving": 82.0
            },
            "skill_analysis": {
                "programming": "Good",
                "algorithms": "Average",
                "communication": "Needs improvement"
            },
            "improvement_areas": [
                "Practice public speaking",
                "Work on time management",
                "Strengthen algorithm skills"
            ],
            "generated_at": "2024-01-01T00:00:00Z",
            "expires_at": "2024-02-01T00:00:00Z",
            "status": "completed"
        }
        
        return ReportResponse(**report_data)
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate report")


@router.get("/report/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific report by ID."""
    try:
        # Mock report data
        report_data = {
            "id": report_id,
            "user_id": 1,
            "report_type": "comprehensive",
            "title": f"Comprehensive Report #{report_id}",
            "description": "Detailed performance analysis and recommendations",
            "content": {
                "summary": "User shows strong potential with areas for improvement",
                "performance_metrics": {
                    "overall_score": 75.5,
                    "assessment_score": 78.0,
                    "interview_score": 72.0
                }
            },
            "summary": "User demonstrates solid technical foundation with room for improvement in soft skills.",
            "recommendations": "Focus on communication skills and practice mock interviews regularly.",
            "overall_score": 75.5,
            "mcq_score": 80.0,
            "coding_score": 75.0,
            "aptitude_score": 70.0,
            "interview_score": 72.0,
            "pdf_file_path": f"/reports/report_{report_id}.pdf",
            "pdf_file_size": 1024000,
            "performance_breakdown": {
                "technical": 78.0,
                "communication": 65.0,
                "problem_solving": 82.0
            },
            "skill_analysis": {
                "programming": "Good",
                "algorithms": "Average",
                "communication": "Needs improvement"
            },
            "improvement_areas": [
                "Practice public speaking",
                "Work on time management",
                "Strengthen algorithm skills"
            ],
            "generated_at": "2024-01-01T00:00:00Z",
            "expires_at": "2024-02-01T00:00:00Z",
            "status": "completed"
        }
        
        return ReportResponse(**report_data)
        
    except Exception as e:
        logger.error(f"Error getting report: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get report")


@router.get("/user/{user_id}/reports", response_model=ReportList)
async def get_user_reports(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all reports for a specific user."""
    try:
        # Mock reports data
        reports = []
        for i in range(min(limit, 5)):  # Mock 5 reports
            report_data = {
                "id": i + 1,
                "user_id": user_id,
                "report_type": "comprehensive" if i % 2 == 0 else "assessment",
                "title": f"Report {i + 1} for User {user_id}",
                "description": f"Report #{i + 1} analysis and recommendations",
                "content": {"summary": "User performance analysis"},
                "summary": "User shows good potential",
                "recommendations": "Continue practicing",
                "overall_score": 75.0 + i * 2,
                "mcq_score": 80.0,
                "coding_score": 75.0,
                "aptitude_score": 70.0,
                "interview_score": 72.0,
                "pdf_file_path": f"/reports/user_{user_id}_report_{i + 1}.pdf",
                "pdf_file_size": 1024000,
                "performance_breakdown": {"technical": 78.0},
                "skill_analysis": {"programming": "Good"},
                "improvement_areas": ["Communication"],
                "generated_at": "2024-01-01T00:00:00Z",
                "expires_at": "2024-02-01T00:00:00Z",
                "status": "completed"
            }
            reports.append(ReportResponse(**report_data))
        
        return ReportList(
            reports=reports,
            total=len(reports),
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting user reports: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user reports")


@router.get("/performance/{user_id}", response_model=PerformanceMetrics)
async def get_performance_metrics(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed performance metrics for a user."""
    try:
        # Get performance summary
        performance_summary = get_user_performance_summary(db, user_id)
        
        if not performance_summary:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Mock performance metrics
        metrics = {
            "user_id": user_id,
            "assessment_metrics": {
                "total_assessments": performance_summary.get("total_assessments", 0),
                "average_score": performance_summary.get("average_assessment_score", 0),
                "best_score": performance_summary.get("best_assessment_score", 0),
                "improvement_rate": 15.5
            },
            "interview_metrics": {
                "total_interviews": performance_summary.get("total_interviews", 0),
                "average_score": performance_summary.get("average_interview_score", 0),
                "best_score": performance_summary.get("best_interview_score", 0),
                "communication_score": 75.0
            },
            "overall_metrics": {
                "overall_score": 76.5,
                "total_time_spent": 3600,
                "completion_rate": 85.0
            },
            "skill_analysis": {
                "technical_skills": 78.0,
                "soft_skills": 72.0,
                "problem_solving": 80.0
            },
            "recommendations": [
                "Practice mock interviews regularly",
                "Focus on communication skills",
                "Work on time management",
                "Strengthen algorithm knowledge"
            ]
        }
        
        return PerformanceMetrics(**metrics)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting performance metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get performance metrics") 