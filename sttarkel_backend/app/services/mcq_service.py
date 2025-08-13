"""
MCQ Service for SttarkelTool backend.
Handles MCQ question generation, assessment creation, and scoring.
"""

import random
from typing import List, Dict, Any, Optional
from app.schemas.assessment import MCQQuestion, MCQSubmission
from app.utils.text_analysis import generate_feedback
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MCQService:
    """Service for handling MCQ assessments."""
    
    def __init__(self):
        """Initialize MCQ service with question bank."""
        self.question_bank = self._load_question_bank()
    
    def _load_question_bank(self) -> Dict[str, List[MCQQuestion]]:
        """Load MCQ questions from question bank."""
        return {
            "programming": [
                MCQQuestion(
                    id="prog_001",
                    question="What is the time complexity of binary search?",
                    options=["O(1)", "O(log n)", "O(n)", "O(n²)"],
                    correct_answer="O(log n)",
                    difficulty="medium",
                    category="algorithms",
                    explanation="Binary search divides the search space in half with each iteration, resulting in logarithmic time complexity."
                ),
                MCQQuestion(
                    id="prog_002",
                    question="Which data structure uses LIFO principle?",
                    options=["Queue", "Stack", "Tree", "Graph"],
                    correct_answer="Stack",
                    difficulty="easy",
                    category="data_structures",
                    explanation="Stack follows Last In First Out (LIFO) principle."
                ),
                MCQQuestion(
                    id="prog_003",
                    question="What is the output of: print(2 ** 3)?",
                    options=["6", "8", "5", "Error"],
                    correct_answer="8",
                    difficulty="easy",
                    category="python",
                    explanation="** is the exponentiation operator in Python."
                ),
                MCQQuestion(
                    id="prog_004",
                    question="Which sorting algorithm has the best average-case time complexity?",
                    options=["Bubble Sort", "Quick Sort", "Selection Sort", "Insertion Sort"],
                    correct_answer="Quick Sort",
                    difficulty="medium",
                    category="algorithms",
                    explanation="Quick Sort has O(n log n) average-case time complexity."
                ),
                MCQQuestion(
                    id="prog_005",
                    question="What is encapsulation in OOP?",
                    options=["Bundling data and methods", "Inheritance", "Polymorphism", "Abstraction"],
                    correct_answer="Bundling data and methods",
                    difficulty="medium",
                    category="oop",
                    explanation="Encapsulation is the bundling of data and methods that operate on that data within a single unit."
                )
            ],
            "aptitude": [
                MCQQuestion(
                    id="apt_001",
                    question="If a train travels 120 km in 2 hours, what is its speed?",
                    options=["40 km/h", "60 km/h", "80 km/h", "100 km/h"],
                    correct_answer="60 km/h",
                    difficulty="easy",
                    category="numerical",
                    explanation="Speed = Distance/Time = 120/2 = 60 km/h"
                ),
                MCQQuestion(
                    id="apt_002",
                    question="Complete the series: 2, 4, 8, 16, __",
                    options=["24", "32", "30", "28"],
                    correct_answer="32",
                    difficulty="medium",
                    category="logical",
                    explanation="Each number is multiplied by 2 to get the next number."
                ),
                MCQQuestion(
                    id="apt_003",
                    question="Which word is most similar to 'Eloquent'?",
                    options=["Quiet", "Articulate", "Confused", "Angry"],
                    correct_answer="Articulate",
                    difficulty="medium",
                    category="verbal",
                    explanation="Eloquent means fluent or persuasive in speaking, similar to articulate."
                ),
                MCQQuestion(
                    id="apt_004",
                    question="If 5 workers can complete a task in 10 days, how many days will 10 workers take?",
                    options=["5 days", "10 days", "15 days", "20 days"],
                    correct_answer="5 days",
                    difficulty="medium",
                    category="numerical",
                    explanation="More workers = less time. Inverse proportion: 5×10 = 10×x, so x=5"
                ),
                MCQQuestion(
                    id="apt_005",
                    question="Which figure comes next: Circle, Square, Triangle, Circle, Square, __",
                    options=["Circle", "Square", "Triangle", "Rectangle"],
                    correct_answer="Triangle",
                    difficulty="easy",
                    category="logical",
                    explanation="The pattern repeats: Circle, Square, Triangle"
                )
            ]
        }
    
    async def generate_mcq_assessment(self, category: str = "programming", difficulty: str = "medium", count: int = 5) -> Dict[str, Any]:
        """Generate an MCQ assessment with specified parameters."""
        try:
            if category not in self.question_bank:
                raise ValueError(f"Category '{category}' not found")
            
            available_questions = self.question_bank[category]
            filtered_questions = [q for q in available_questions if q.difficulty == difficulty]
            
            if len(filtered_questions) < count:
                # If not enough questions of specified difficulty, include others
                filtered_questions = available_questions
            
            selected_questions = random.sample(filtered_questions, min(count, len(filtered_questions)))
            
            # Create assessment structure
            assessment_data = {
                "questions": [q.dict() for q in selected_questions],
                "correct_answers": {q.id: q.correct_answer for q in selected_questions},
                "max_score": len(selected_questions),
                "total_questions": len(selected_questions),
                "category": category,
                "difficulty": difficulty
            }
            
            logger.info(f"Generated MCQ assessment: {category}, {difficulty}, {count} questions")
            return assessment_data
            
        except Exception as e:
            logger.error(f"Error generating MCQ assessment: {str(e)}")
            raise
    
    async def evaluate_mcq_submission(self, submission: MCQSubmission, correct_answers: Dict[str, str]) -> Dict[str, Any]:
        """Evaluate MCQ submission and return results."""
        try:
            user_answers = submission.answers
            score = 0
            correct_count = 0
            detailed_results = []
            
            for question_id, correct_answer in correct_answers.items():
                user_answer = user_answers.get(question_id, "")
                is_correct = user_answer == correct_answer
                
                if is_correct:
                    score += 1
                    correct_count += 1
                
                detailed_results.append({
                    "question_id": question_id,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct
                })
            
            max_score = len(correct_answers)
            percentage = (score / max_score * 100) if max_score > 0 else 0
            
            # Generate feedback
            feedback = await self._generate_mcq_feedback(score, max_score, detailed_results)
            
            result = {
                "score": score,
                "max_score": max_score,
                "percentage": round(percentage, 2),
                "correct_count": correct_count,
                "total_questions": max_score,
                "time_taken": submission.time_taken or 0,
                "detailed_results": detailed_results,
                "feedback": feedback["feedback"],
                "strengths": feedback["strengths"],
                "weaknesses": feedback["weaknesses"],
                "recommendations": feedback["recommendations"]
            }
            
            logger.info(f"Evaluated MCQ submission: {score}/{max_score} ({percentage}%)")
            return result
            
        except Exception as e:
            logger.error(f"Error evaluating MCQ submission: {str(e)}")
            raise
    
    async def _generate_mcq_feedback(self, score: int, max_score: int, detailed_results: List[Dict]) -> Dict[str, Any]:
        """Generate feedback for MCQ assessment."""
        percentage = (score / max_score * 100) if max_score > 0 else 0
        
        # Analyze performance
        if percentage >= 80:
            performance_level = "excellent"
            strengths = ["Strong understanding of concepts", "Good analytical skills"]
            weaknesses = []
        elif percentage >= 60:
            performance_level = "good"
            strengths = ["Solid foundation", "Good problem-solving approach"]
            weaknesses = ["Some concepts need reinforcement"]
        elif percentage >= 40:
            performance_level = "fair"
            strengths = ["Basic understanding present"]
            weaknesses = ["Several concepts need improvement", "More practice required"]
        else:
            performance_level = "needs_improvement"
            strengths = []
            weaknesses = ["Fundamental concepts need work", "Extensive practice required"]
        
        # Generate recommendations
        recommendations = []
        if percentage < 80:
            recommendations.append("Review incorrect answers and understand the explanations")
        if percentage < 60:
            recommendations.append("Focus on strengthening core concepts")
        if percentage < 40:
            recommendations.append("Consider taking foundational courses")
        
        recommendations.append("Practice regularly with similar questions")
        recommendations.append("Time management can be improved")
        
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
    
    async def get_questions_by_category(self, category: str) -> List[MCQQuestion]:
        """Get questions by category."""
        return self.question_bank.get(category, [])
    
    async def add_question(self, category: str, question: MCQQuestion) -> bool:
        """Add a new question to the question bank."""
        try:
            if category not in self.question_bank:
                self.question_bank[category] = []
            
            self.question_bank[category].append(question)
            logger.info(f"Added new MCQ question: {question.id} to category {category}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding MCQ question: {str(e)}")
            return False


# Global MCQ service instance
mcq_service = MCQService() 