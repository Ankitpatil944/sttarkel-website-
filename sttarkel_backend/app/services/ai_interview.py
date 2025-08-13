"""
AI Interview Service for SttarkelTool backend.
Handles Tavus CVI session creation, management, and feedback generation.
"""

import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.schemas.interview import TavusPersona, TavusSessionRequest, TavusSessionResponse, TavusTranscript
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AIInterviewService:
    """Service for handling AI-driven interviews using Tavus CVI."""
    
    def __init__(self):
        """Initialize AI interview service."""
        self.tavus_base_url = settings.tavus_base_url
        self.api_key = settings.tavus_api_key
        self.timeout = settings.tavus_timeout
        
        # Mock personas for development/testing
        self.mock_personas = [
            TavusPersona(
                id="tech_lead_001",
                name="Sarah Chen",
                description="Senior Tech Lead at Google with 8+ years of experience in software engineering",
                role="Tech Lead",
                company="Google",
                industry="Technology",
                difficulty="hard",
                specialties=["System Design", "Leadership", "Technical Architecture"],
                avatar_url="https://example.com/avatars/sarah_chen.jpg"
            ),
            TavusPersona(
                id="senior_dev_001",
                name="Michael Rodriguez",
                description="Senior Software Engineer at Microsoft specializing in backend development",
                role="Senior Software Engineer",
                company="Microsoft",
                industry="Technology",
                difficulty="medium",
                specialties=["Backend Development", "Database Design", "API Development"],
                avatar_url="https://example.com/avatars/michael_rodriguez.jpg"
            ),
            TavusPersona(
                id="junior_dev_001",
                name="Emily Johnson",
                description="Junior Developer at a startup with 2 years of experience in full-stack development",
                role="Junior Developer",
                company="Tech Startup",
                industry="Technology",
                difficulty="easy",
                specialties=["Full-stack Development", "React", "Node.js"],
                avatar_url="https://example.com/avatars/emily_johnson.jpg"
            ),
            TavusPersona(
                id="hr_manager_001",
                name="David Thompson",
                description="HR Manager at Amazon with expertise in technical hiring and candidate evaluation",
                role="HR Manager",
                company="Amazon",
                industry="Technology",
                difficulty="medium",
                specialties=["Behavioral Questions", "Culture Fit", "Soft Skills"],
                avatar_url="https://example.com/avatars/david_thompson.jpg"
            ),
            TavusPersona(
                id="product_manager_001",
                name="Lisa Wang",
                description="Product Manager at Facebook with experience in product strategy and user experience",
                role="Product Manager",
                company="Facebook",
                industry="Technology",
                difficulty="medium",
                specialties=["Product Strategy", "User Experience", "Data Analysis"],
                avatar_url="https://example.com/avatars/lisa_wang.jpg"
            )
        ]
    
    async def get_available_personas(self) -> List[TavusPersona]:
        """Get list of available Tavus personas."""
        try:
            if self.api_key:
                return await self._get_tavus_personas()
            else:
                # Return mock personas for development
                return self.mock_personas
                
        except Exception as e:
            logger.error(f"Error getting personas: {str(e)}")
            # Fallback to mock personas
            return self.mock_personas
    
    async def _get_tavus_personas(self) -> List[TavusPersona]:
        """Get personas from Tavus API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.tavus_base_url}/personas",
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [TavusPersona(**persona) for persona in data.get("personas", [])]
                    else:
                        logger.warning(f"Failed to get Tavus personas: {response.status}")
                        return self.mock_personas
                        
        except Exception as e:
            logger.error(f"Error fetching Tavus personas: {str(e)}")
            return self.mock_personas
    
    async def create_interview_session(self, request: TavusSessionRequest) -> TavusSessionResponse:
        """Create a new Tavus CVI interview session."""
        try:
            if self.api_key:
                return await self._create_tavus_session(request)
            else:
                return await self._create_mock_session(request)
                
        except Exception as e:
            logger.error(f"Error creating interview session: {str(e)}")
            raise
    
    async def _create_tavus_session(self, request: TavusSessionRequest) -> TavusSessionResponse:
        """Create session using Tavus API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            session_data = {
                "persona_id": request.persona_id,
                "user_name": request.user_name,
                "user_email": request.user_email,
                "session_duration": request.session_duration,
                "custom_questions": request.custom_questions or []
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.tavus_base_url}/sessions",
                    headers=headers,
                    json=session_data,
                    timeout=self.timeout
                ) as response:
                    if response.status == 201:
                        data = await response.json()
                        return TavusSessionResponse(
                            session_id=data["session_id"],
                            session_url=data["session_url"],
                            status="created",
                            created_at=datetime.utcnow(),
                            expires_at=datetime.utcnow() + timedelta(hours=24)
                        )
                    else:
                        raise Exception(f"Failed to create Tavus session: {response.status}")
                        
        except Exception as e:
            logger.error(f"Error creating Tavus session: {str(e)}")
            raise
    
    async def _create_mock_session(self, request: TavusSessionRequest) -> TavusSessionResponse:
        """Create mock session for development/testing."""
        import uuid
        
        session_id = str(uuid.uuid4())
        session_url = f"https://mock-tavus.com/session/{session_id}"
        
        return TavusSessionResponse(
            session_id=session_id,
            session_url=session_url,
            status="created",
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
    
    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get the status of an interview session."""
        try:
            if self.api_key:
                return await self._get_tavus_session_status(session_id)
            else:
                return await self._get_mock_session_status(session_id)
                
        except Exception as e:
            logger.error(f"Error getting session status: {str(e)}")
            raise
    
    async def _get_tavus_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get session status from Tavus API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.tavus_base_url}/sessions/{session_id}",
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise Exception(f"Failed to get session status: {response.status}")
                        
        except Exception as e:
            logger.error(f"Error getting Tavus session status: {str(e)}")
            raise
    
    async def _get_mock_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get mock session status for development/testing."""
        import random
        
        statuses = ["active", "completed", "expired"]
        status = random.choice(statuses)
        
        return {
            "session_id": session_id,
            "status": status,
            "created_at": datetime.utcnow().isoformat(),
            "duration": random.randint(300, 1800),  # 5-30 minutes
            "questions_asked": random.randint(5, 15),
            "completion_percentage": random.randint(0, 100)
        }
    
    async def get_session_transcript(self, session_id: str) -> TavusTranscript:
        """Get the transcript of an interview session."""
        try:
            if self.api_key:
                return await self._get_tavus_transcript(session_id)
            else:
                return await self._get_mock_transcript(session_id)
                
        except Exception as e:
            logger.error(f"Error getting session transcript: {str(e)}")
            raise
    
    async def _get_tavus_transcript(self, session_id: str) -> TavusTranscript:
        """Get transcript from Tavus API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.tavus_base_url}/sessions/{session_id}/transcript",
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return TavusTranscript(**data)
                    else:
                        raise Exception(f"Failed to get transcript: {response.status}")
                        
        except Exception as e:
            logger.error(f"Error getting Tavus transcript: {str(e)}")
            raise
    
    async def _get_mock_transcript(self, session_id: str) -> TavusTranscript:
        """Get mock transcript for development/testing."""
        questions = [
            "Tell me about yourself and your background.",
            "What are your greatest strengths and weaknesses?",
            "Why are you interested in this position?",
            "Describe a challenging project you worked on.",
            "How do you handle working under pressure?",
            "What are your career goals for the next 5 years?",
            "How do you stay updated with industry trends?",
            "Describe a time when you had to learn something quickly.",
            "How do you handle conflicts in a team?",
            "What questions do you have for me?"
        ]
        
        responses = [
            "I'm a software engineer with 3 years of experience in full-stack development...",
            "My greatest strength is my problem-solving ability, and I'm working on improving my public speaking...",
            "I'm excited about the opportunity to work on cutting-edge technology...",
            "I worked on a complex e-commerce platform that required integrating multiple payment systems...",
            "I prioritize tasks and maintain clear communication with stakeholders...",
            "I want to grow into a technical leadership role and mentor junior developers...",
            "I follow industry blogs, attend conferences, and participate in online courses...",
            "When I needed to learn React quickly, I created a personal project and practiced daily...",
            "I focus on understanding different perspectives and finding common ground...",
            "I'd like to learn more about the team structure and growth opportunities..."
        ]
        
        # Generate mock conversation
        conversation = []
        for i in range(min(len(questions), len(responses))):
            conversation.append(f"Interviewer: {questions[i]}")
            conversation.append(f"Candidate: {responses[i]}")
        
        transcript_text = "\n".join(conversation)
        
        return TavusTranscript(
            session_id=session_id,
            transcript=transcript_text,
            duration=random.randint(600, 1800),  # 10-30 minutes
            questions_asked=questions[:5],
            user_responses=responses[:5],
            analysis={
                "communication_score": random.randint(70, 95),
                "technical_score": random.randint(65, 90),
                "confidence_score": random.randint(60, 85),
                "overall_score": random.randint(65, 90)
            }
        )
    
    async def generate_interview_feedback(self, transcript: TavusTranscript) -> Dict[str, Any]:
        """Generate comprehensive feedback from interview transcript."""
        try:
            # Analyze transcript using AI or predefined patterns
            analysis = transcript.analysis or await self._analyze_transcript(transcript.transcript)
            
            # Generate detailed feedback
            feedback = await self._generate_detailed_feedback(analysis)
            
            return {
                "communication_score": analysis.get("communication_score", 0),
                "technical_score": analysis.get("technical_score", 0),
                "confidence_score": analysis.get("confidence_score", 0),
                "overall_score": analysis.get("overall_score", 0),
                "feedback": feedback["feedback"],
                "strengths": feedback["strengths"],
                "areas_for_improvement": feedback["areas_for_improvement"],
                "recommendations": feedback["recommendations"],
                "transcript": transcript.transcript,
                "questions_asked": transcript.questions_asked,
                "user_responses": transcript.user_responses
            }
            
        except Exception as e:
            logger.error(f"Error generating interview feedback: {str(e)}")
            raise
    
    async def _analyze_transcript(self, transcript: str) -> Dict[str, Any]:
        """Analyze transcript to extract scores and insights."""
        # This would typically use an AI service like OpenAI or Gemini
        # For now, we'll use a simple analysis based on keywords and patterns
        
        transcript_lower = transcript.lower()
        
        # Communication analysis
        communication_indicators = {
            "positive": ["clear", "articulate", "confident", "professional", "well-structured"],
            "negative": ["um", "uh", "like", "you know", "hesitant", "unclear"]
        }
        
        communication_score = 75  # Base score
        for word in communication_indicators["positive"]:
            if word in transcript_lower:
                communication_score += 2
        for word in communication_indicators["negative"]:
            if word in transcript_lower:
                communication_score -= 3
        
        # Technical analysis
        technical_indicators = {
            "positive": ["algorithm", "architecture", "optimization", "scalability", "database", "api"],
            "negative": ["don't know", "not sure", "maybe", "probably"]
        }
        
        technical_score = 70  # Base score
        for word in technical_indicators["positive"]:
            if word in transcript_lower:
                technical_score += 3
        for word in technical_indicators["negative"]:
            if word in transcript_lower:
                technical_score -= 2
        
        # Confidence analysis
        confidence_score = 80  # Base score
        if "confident" in transcript_lower or "sure" in transcript_lower:
            confidence_score += 5
        if "hesitant" in transcript_lower or "unsure" in transcript_lower:
            confidence_score -= 10
        
        # Calculate overall score
        overall_score = (communication_score + technical_score + confidence_score) / 3
        
        return {
            "communication_score": max(0, min(100, communication_score)),
            "technical_score": max(0, min(100, technical_score)),
            "confidence_score": max(0, min(100, confidence_score)),
            "overall_score": max(0, min(100, overall_score))
        }
    
    async def _generate_detailed_feedback(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed feedback based on analysis."""
        communication_score = analysis.get("communication_score", 0)
        technical_score = analysis.get("technical_score", 0)
        confidence_score = analysis.get("confidence_score", 0)
        overall_score = analysis.get("overall_score", 0)
        
        # Generate strengths
        strengths = []
        if communication_score >= 80:
            strengths.append("Excellent communication skills")
        elif communication_score >= 70:
            strengths.append("Good communication skills")
        
        if technical_score >= 80:
            strengths.append("Strong technical knowledge")
        elif technical_score >= 70:
            strengths.append("Solid technical foundation")
        
        if confidence_score >= 80:
            strengths.append("High confidence and poise")
        elif confidence_score >= 70:
            strengths.append("Good confidence level")
        
        # Generate areas for improvement
        areas_for_improvement = []
        if communication_score < 70:
            areas_for_improvement.append("Work on clarity and articulation")
        if technical_score < 70:
            areas_for_improvement.append("Strengthen technical knowledge")
        if confidence_score < 70:
            areas_for_improvement.append("Build confidence through practice")
        
        # Generate recommendations
        recommendations = []
        if communication_score < 80:
            recommendations.append("Practice speaking clearly and avoiding filler words")
        if technical_score < 80:
            recommendations.append("Review technical concepts and stay updated with industry trends")
        if confidence_score < 80:
            recommendations.append("Practice mock interviews to build confidence")
        
        recommendations.append("Prepare specific examples for behavioral questions")
        recommendations.append("Research the company and role thoroughly")
        
        # Generate feedback text
        feedback_text = f"Overall Score: {overall_score:.1f}/100. "
        feedback_text += f"Communication: {communication_score:.1f}/100, "
        feedback_text += f"Technical: {technical_score:.1f}/100, "
        feedback_text += f"Confidence: {confidence_score:.1f}/100. "
        
        if strengths:
            feedback_text += f"Strengths: {', '.join(strengths)}. "
        if areas_for_improvement:
            feedback_text += f"Areas for improvement: {', '.join(areas_for_improvement)}."
        
        return {
            "feedback": feedback_text,
            "strengths": strengths,
            "areas_for_improvement": areas_for_improvement,
            "recommendations": recommendations
        }
    
    async def get_persona_by_id(self, persona_id: str) -> Optional[TavusPersona]:
        """Get a specific persona by ID."""
        personas = await self.get_available_personas()
        for persona in personas:
            if persona.id == persona_id:
                return persona
        return None


# Global AI interview service instance
ai_interview_service = AIInterviewService() 