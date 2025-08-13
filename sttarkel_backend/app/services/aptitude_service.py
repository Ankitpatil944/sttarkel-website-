"""
Aptitude Service for SttarkelTool backend.
Handles aptitude question generation, assessment creation, and scoring.
"""

import random
from typing import List, Dict, Any, Optional
from app.schemas.assessment import AptitudeQuestion, AptitudeSubmission
from app.utils.text_analysis import generate_feedback
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AptitudeService:
    """Service for handling aptitude assessments."""
    
    def __init__(self):
        """Initialize aptitude service with question bank."""
        self.question_bank = self._load_question_bank()
    
    def _load_question_bank(self) -> Dict[str, List[AptitudeQuestion]]:
        """Load aptitude questions from question bank."""
        return {
            "numerical": [
                AptitudeQuestion(
                    id="num_001",
                    question="If a train travels 120 km in 2 hours, what is its speed?",
                    options=["40 km/h", "60 km/h", "80 km/h", "100 km/h"],
                    correct_answer="60 km/h",
                    category="numerical",
                    difficulty="easy"
                ),
                AptitudeQuestion(
                    id="num_002",
                    question="If 5 workers can complete a task in 10 days, how many days will 10 workers take?",
                    options=["5 days", "10 days", "15 days", "20 days"],
                    correct_answer="5 days",
                    category="numerical",
                    difficulty="medium"
                ),
                AptitudeQuestion(
                    id="num_003",
                    question="A shopkeeper sells an item for $120 and makes a 20% profit. What was the cost price?",
                    options=["$90", "$100", "$110", "$130"],
                    correct_answer="$100",
                    category="numerical",
                    difficulty="medium"
                )
            ],
            "logical": [
                AptitudeQuestion(
                    id="log_001",
                    question="Complete the series: 2, 4, 8, 16, __",
                    options=["24", "32", "30", "28"],
                    correct_answer="32",
                    category="logical",
                    difficulty="medium"
                ),
                AptitudeQuestion(
                    id="log_002",
                    question="Which figure comes next: Circle, Square, Triangle, Circle, Square, __",
                    options=["Circle", "Square", "Triangle", "Rectangle"],
                    correct_answer="Triangle",
                    category="logical",
                    difficulty="easy"
                ),
                AptitudeQuestion(
                    id="log_003",
                    question="If all roses are flowers and some flowers are red, then:",
                    options=["All roses are red", "Some roses are red", "No roses are red", "Cannot be determined"],
                    correct_answer="Cannot be determined",
                    category="logical",
                    difficulty="hard"
                )
            ],
            "verbal": [
                AptitudeQuestion(
                    id="verb_001",
                    question="Which word is most similar to 'Eloquent'?",
                    options=["Quiet", "Articulate", "Confused", "Angry"],
                    correct_answer="Articulate",
                    category="verbal",
                    difficulty="medium"
                ),
                AptitudeQuestion(
                    id="verb_002",
                    question="Choose the word that best completes the sentence: The weather was so ___ that we had to cancel the picnic.",
                    options=["pleasant", "inclement", "sunny", "warm"],
                    correct_answer="inclement",
                    category="verbal",
                    difficulty="medium"
                ),
                AptitudeQuestion(
                    id="verb_003",
                    question="Which word is the opposite of 'Ubiquitous'?",
                    options=["Common", "Rare", "Popular", "Famous"],
                    correct_answer="Rare",
                    category="verbal",
                    difficulty="hard"
                )
            ]
        }
    
    async def generate_aptitude_assessment(self, difficulty: str = "medium", count: int = 10) -> Dict[str, Any]:
        """Generate an aptitude assessment with specified parameters."""
        try:
            # Select questions from different categories
            questions = []
            categories = list(self.question_bank.keys())
            questions_per_category = count // len(categories)
            remaining = count % len(categories)
            
            for i, category in enumerate(categories):
                category_questions = self.question_bank[category]
                filtered_questions = [q for q in category_questions if q.difficulty == difficulty]
                
                if len(filtered_questions) < questions_per_category:
                    filtered_questions = category_questions
                
                # Add extra questions to the first few categories if there are remaining
                extra = 1 if i < remaining else 0
                selected_count = questions_per_category + extra
                
                selected = random.sample(filtered_questions, min(selected_count, len(filtered_questions)))
                questions.extend(selected)
            
            # Shuffle questions
            random.shuffle(questions)
            
            # Create assessment structure
            assessment_data = {
                "questions": [q.dict() for q in questions],
                "correct_answers": {q.id: q.correct_answer for q in questions},
                "max_score": len(questions),
                "total_questions": len(questions),
                "difficulty": difficulty
            }
            
            logger.info(f"Generated aptitude assessment: {difficulty}, {count} questions")
            return assessment_data
            
        except Exception as e:
            logger.error(f"Error generating aptitude assessment: {str(e)}")
            raise
    
    async def evaluate_aptitude_submission(self, submission: AptitudeSubmission, correct_answers: Dict[str, str]) -> Dict[str, Any]:
        """Evaluate aptitude submission and return results."""
        try:
            user_answers = submission.answers
            score = 0
            correct_count = 0
            detailed_results = []
            category_scores = {}
            
            for question_id, correct_answer in correct_answers.items():
                user_answer = user_answers.get(question_id, "")
                is_correct = user_answer == correct_answer
                
                if is_correct:
                    score += 1
                    correct_count += 1
                
                # Get question category for detailed analysis
                question_category = self._get_question_category(question_id)
                if question_category:
                    if question_category not in category_scores:
                        category_scores[question_category] = {"correct": 0, "total": 0}
                    category_scores[question_category]["total"] += 1
                    if is_correct:
                        category_scores[question_category]["correct"] += 1
                
                detailed_results.append({
                    "question_id": question_id,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct,
                    "category": question_category
                })
            
            max_score = len(correct_answers)
            percentage = (score / max_score * 100) if max_score > 0 else 0
            
            # Calculate category-wise scores
            category_performance = {}
            for category, scores in category_scores.items():
                category_performance[category] = (scores["correct"] / scores["total"] * 100) if scores["total"] > 0 else 0
            
            # Generate feedback
            feedback = await self._generate_aptitude_feedback(score, max_score, category_performance, detailed_results)
            
            result = {
                "score": score,
                "max_score": max_score,
                "percentage": round(percentage, 2),
                "correct_count": correct_count,
                "total_questions": max_score,
                "time_taken": submission.time_taken or 0,
                "detailed_results": detailed_results,
                "category_performance": category_performance,
                "feedback": feedback["feedback"],
                "strengths": feedback["strengths"],
                "weaknesses": feedback["weaknesses"],
                "recommendations": feedback["recommendations"]
            }
            
            logger.info(f"Evaluated aptitude submission: {score}/{max_score} ({percentage}%)")
            return result
            
        except Exception as e:
            logger.error(f"Error evaluating aptitude submission: {str(e)}")
            raise
    
    def _get_question_category(self, question_id: str) -> Optional[str]:
        """Get the category of a question by its ID."""
        for category, questions in self.question_bank.items():
            for question in questions:
                if question.id == question_id:
                    return category
        return None
    
    async def _generate_aptitude_feedback(self, score: int, max_score: int, category_performance: Dict[str, float], detailed_results: List[Dict]) -> Dict[str, Any]:
        """Generate feedback for aptitude assessment."""
        percentage = (score / max_score * 100) if max_score > 0 else 0
        
        # Analyze performance by category
        strengths = []
        weaknesses = []
        
        for category, cat_score in category_performance.items():
            if cat_score >= 80:
                strengths.append(f"Strong {category} reasoning skills")
            elif cat_score < 60:
                weaknesses.append(f"Needs improvement in {category} reasoning")
        
        # Overall performance analysis
        if percentage >= 80:
            performance_level = "excellent"
            if not strengths:
                strengths.append("Strong overall aptitude")
        elif percentage >= 60:
            performance_level = "good"
            if not strengths:
                strengths.append("Good foundation in aptitude")
        elif percentage >= 40:
            performance_level = "fair"
            if not strengths:
                strengths.append("Basic aptitude skills present")
        else:
            performance_level = "needs_improvement"
            if not weaknesses:
                weaknesses.append("Fundamental aptitude skills need work")
        
        # Generate recommendations
        recommendations = []
        if percentage < 80:
            recommendations.append("Practice aptitude questions regularly")
        if percentage < 60:
            recommendations.append("Focus on weak areas identified in the assessment")
        if percentage < 40:
            recommendations.append("Consider taking aptitude preparation courses")
        
        # Category-specific recommendations
        for category, cat_score in category_performance.items():
            if cat_score < 70:
                if category == "numerical":
                    recommendations.append("Practice mathematical reasoning and problem-solving")
                elif category == "logical":
                    recommendations.append("Work on pattern recognition and logical thinking")
                elif category == "verbal":
                    recommendations.append("Improve vocabulary and verbal reasoning skills")
        
        recommendations.append("Time management is crucial for aptitude tests")
        recommendations.append("Read questions carefully before answering")
        
        feedback_text = f"You scored {score}/{max_score} ({percentage}%). Your performance is {performance_level}. "
        if strengths:
            feedback_text += f"Strengths: {', '.join(strengths)}. "
        if weaknesses:
            feedback_text += f"Areas for improvement: {', '.join(weaknesses)}."
        
        return {
            "feedback": feedback_text,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }
    
    async def get_question_categories(self) -> List[str]:
        """Get available question categories."""
        return list(self.question_bank.keys())
    
    async def get_questions_by_category(self, category: str) -> List[AptitudeQuestion]:
        """Get questions by category."""
        return self.question_bank.get(category, [])
    
    async def add_question(self, category: str, question: AptitudeQuestion) -> bool:
        """Add a new question to the question bank."""
        try:
            if category not in self.question_bank:
                self.question_bank[category] = []
            
            self.question_bank[category].append(question)
            logger.info(f"Added new aptitude question: {question.id} to category {category}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding aptitude question: {str(e)}")
            return False


# Global aptitude service instance
aptitude_service = AptitudeService() 