"""
Text analysis utility for SttarkelTool backend.
Provides feedback generation and text analysis capabilities.
"""

import re
from typing import List, Dict, Any, Optional
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def generate_feedback(score: float, max_score: float, assessment_type: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate comprehensive feedback based on assessment results.
    
    Args:
        score: User's score
        max_score: Maximum possible score
        assessment_type: Type of assessment (mcq, coding, aptitude, interview)
        details: Additional details about the assessment
    
    Returns:
        Dictionary containing feedback, strengths, weaknesses, and recommendations
    """
    try:
        percentage = (score / max_score * 100) if max_score > 0 else 0
        
        # Generate base feedback
        feedback_data = await _generate_base_feedback(percentage, assessment_type)
        
        # Add specific feedback based on assessment type
        if assessment_type == "mcq":
            feedback_data.update(await _generate_mcq_feedback(percentage, details))
        elif assessment_type == "coding":
            feedback_data.update(await _generate_coding_feedback(percentage, details))
        elif assessment_type == "aptitude":
            feedback_data.update(await _generate_aptitude_feedback(percentage, details))
        elif assessment_type == "interview":
            feedback_data.update(await _generate_interview_feedback(percentage, details))
        
        return feedback_data
        
    except Exception as e:
        logger.error(f"Error generating feedback: {str(e)}")
        return _get_default_feedback()


async def _generate_base_feedback(percentage: float, assessment_type: str) -> Dict[str, Any]:
    """Generate base feedback based on performance percentage."""
    
    if percentage >= 90:
        performance_level = "exceptional"
        strengths = ["Outstanding performance", "Excellent understanding of concepts"]
        weaknesses = []
        recommendations = ["Continue maintaining this high standard", "Consider mentoring others"]
    elif percentage >= 80:
        performance_level = "excellent"
        strengths = ["Strong performance", "Good grasp of concepts"]
        weaknesses = ["Minor areas for improvement"]
        recommendations = ["Focus on the few areas that need attention", "Practice advanced concepts"]
    elif percentage >= 70:
        performance_level = "good"
        strengths = ["Solid performance", "Good foundation"]
        weaknesses = ["Some concepts need reinforcement"]
        recommendations = ["Review incorrect answers", "Practice weak areas"]
    elif percentage >= 60:
        performance_level = "fair"
        strengths = ["Basic understanding present"]
        weaknesses = ["Several areas need improvement", "More practice required"]
        recommendations = ["Focus on fundamental concepts", "Increase practice frequency"]
    elif percentage >= 50:
        performance_level = "below_average"
        strengths = ["Some basic knowledge"]
        weaknesses = ["Significant gaps in understanding", "Fundamental concepts missing"]
        recommendations = ["Start with basics", "Consider foundational courses"]
    else:
        performance_level = "needs_improvement"
        strengths = []
        weaknesses = ["Major gaps in knowledge", "Fundamental understanding required"]
        recommendations = ["Begin with basic concepts", "Seek additional learning resources"]
    
    feedback_text = f"Your performance is {performance_level} ({percentage:.1f}%). "
    if strengths:
        feedback_text += f"Strengths: {', '.join(strengths)}. "
    if weaknesses:
        feedback_text += f"Areas for improvement: {', '.join(weaknesses)}."
    
    return {
        "feedback": feedback_text,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "performance_level": performance_level
    }


async def _generate_mcq_feedback(percentage: float, details: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate specific feedback for MCQ assessments."""
    additional_recommendations = [
        "Review explanations for incorrect answers",
        "Practice time management",
        "Read questions carefully before answering",
        "Eliminate obviously wrong options first"
    ]
    
    if details and "category_performance" in details:
        category_feedback = []
        for category, score in details["category_performance"].items():
            if score < 70:
                category_feedback.append(f"Focus on improving {category} knowledge")
        
        if category_feedback:
            additional_recommendations.extend(category_feedback)
    
    return {
        "additional_recommendations": additional_recommendations
    }


async def _generate_coding_feedback(percentage: float, details: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate specific feedback for coding assessments."""
    additional_recommendations = [
        "Practice coding problems regularly",
        "Focus on algorithm efficiency",
        "Test your code with edge cases",
        "Learn common data structures and algorithms"
    ]
    
    if details and "test_results" in details:
        failed_tests = [result for result in details["test_results"] if not result.get("passed", False)]
        if failed_tests:
            additional_recommendations.append(f"Review {len(failed_tests)} failed test cases")
    
    if details and "execution_time" in details:
        exec_time = details["execution_time"]
        if exec_time > 5.0:  # More than 5 seconds
            additional_recommendations.append("Work on optimizing code performance")
    
    return {
        "additional_recommendations": additional_recommendations
    }


async def _generate_aptitude_feedback(percentage: float, details: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate specific feedback for aptitude assessments."""
    additional_recommendations = [
        "Practice logical reasoning problems",
        "Improve mathematical skills",
        "Work on verbal comprehension",
        "Practice pattern recognition"
    ]
    
    if details and "section_scores" in details:
        sections = details["section_scores"]
        for section, score in sections.items():
            if score < 60:
                additional_recommendations.append(f"Focus on improving {section} skills")
    
    return {
        "additional_recommendations": additional_recommendations
    }


async def _generate_interview_feedback(percentage: float, details: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate specific feedback for interview assessments."""
    additional_recommendations = [
        "Practice mock interviews regularly",
        "Prepare specific examples for behavioral questions",
        "Work on communication skills",
        "Research companies before interviews"
    ]
    
    if details and "communication_score" in details:
        comm_score = details["communication_score"]
        if comm_score < 70:
            additional_recommendations.append("Focus on improving verbal communication")
    
    if details and "technical_score" in details:
        tech_score = details["technical_score"]
        if tech_score < 70:
            additional_recommendations.append("Strengthen technical knowledge for interviews")
    
    return {
        "additional_recommendations": additional_recommendations
    }


def _get_default_feedback() -> Dict[str, Any]:
    """Return default feedback when generation fails."""
    return {
        "feedback": "Thank you for completing the assessment. Please review your answers and practice regularly.",
        "strengths": ["Completed the assessment"],
        "weaknesses": ["Unable to analyze performance"],
        "recommendations": ["Practice regularly", "Review concepts", "Seek help if needed"],
        "performance_level": "unknown"
    }


async def analyze_text_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of text (basic implementation).
    
    Args:
        text: Text to analyze
    
    Returns:
        Dictionary with sentiment analysis results
    """
    try:
        text_lower = text.lower()
        
        # Simple sentiment analysis based on keywords
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "perfect", "outstanding"]
        negative_words = ["bad", "terrible", "awful", "horrible", "disappointing", "poor", "worst"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.9, (positive_count - negative_count) / max(positive_count + negative_count, 1))
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.9, (negative_count - positive_count) / max(positive_count + negative_count, 1))
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "positive_count": positive_count,
            "negative_count": negative_count
        }
        
    except Exception as e:
        logger.error(f"Error analyzing text sentiment: {str(e)}")
        return {
            "sentiment": "neutral",
            "confidence": 0.0,
            "positive_count": 0,
            "negative_count": 0
        }


async def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text.
    
    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords to return
    
    Returns:
        List of keywords
    """
    try:
        # Remove common words and punctuation
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"}
        
        # Clean text
        text_clean = re.sub(r'[^\w\s]', '', text.lower())
        words = text_clean.split()
        
        # Filter out stop words and short words
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count frequency
        word_freq = {}
        for word in keywords:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_keywords[:max_keywords]]
        
    except Exception as e:
        logger.error(f"Error extracting keywords: {str(e)}")
        return []


async def generate_summary(text: str, max_length: int = 200) -> str:
    """
    Generate a summary of text.
    
    Args:
        text: Text to summarize
        max_length: Maximum length of summary
    
    Returns:
        Summary text
    """
    try:
        # Simple summary: take first few sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        summary = ""
        for sentence in sentences:
            if len(summary + sentence) <= max_length:
                summary += sentence + ". "
            else:
                break
        
        return summary.strip() if summary else text[:max_length] + "..."
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return text[:max_length] + "..." if len(text) > max_length else text


async def analyze_technical_content(text: str) -> Dict[str, Any]:
    """
    Analyze technical content in text.
    
    Args:
        text: Text to analyze
    
    Returns:
        Dictionary with technical analysis results
    """
    try:
        text_lower = text.lower()
        
        # Technical indicators
        technical_terms = {
            "programming": ["algorithm", "data structure", "api", "database", "framework", "library", "syntax", "compiler", "debugger"],
            "software_engineering": ["architecture", "design pattern", "testing", "deployment", "version control", "agile", "scrum"],
            "web_development": ["html", "css", "javascript", "react", "angular", "vue", "node.js", "express", "django"],
            "databases": ["sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "indexing", "query"],
            "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "microservices", "serverless"]
        }
        
        analysis = {}
        for category, terms in technical_terms.items():
            count = sum(1 for term in terms if term in text_lower)
            analysis[category] = count
        
        total_technical_terms = sum(analysis.values())
        technical_density = total_technical_terms / max(len(text.split()), 1)
        
        return {
            "technical_terms": analysis,
            "total_technical_terms": total_technical_terms,
            "technical_density": technical_density,
            "is_technical": technical_density > 0.01  # 1% threshold
        }
        
    except Exception as e:
        logger.error(f"Error analyzing technical content: {str(e)}")
        return {
            "technical_terms": {},
            "total_technical_terms": 0,
            "technical_density": 0.0,
            "is_technical": False
        } 