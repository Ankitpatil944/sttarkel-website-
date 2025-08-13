"""
Company routes for SttarkelTool backend.
Handles company-specific interview data and flows.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional

from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/list")
async def get_companies():
    """Get list of companies with interview data."""
    try:
        companies = [
            {
                "id": "google",
                "name": "Google",
                "industry": "Technology",
                "size": "Large",
                "location": "Mountain View, CA",
                "description": "Leading technology company specializing in search, cloud computing, and AI",
                "website": "https://google.com",
                "logo_url": "https://example.com/logos/google.png",
                "difficulty": "hard",
                "interview_rounds": 5,
                "average_duration": "2-3 months"
            },
            {
                "id": "microsoft",
                "name": "Microsoft",
                "industry": "Technology",
                "size": "Large",
                "location": "Redmond, WA",
                "description": "Global technology company focused on software, cloud services, and hardware",
                "website": "https://microsoft.com",
                "logo_url": "https://example.com/logos/microsoft.png",
                "difficulty": "hard",
                "interview_rounds": 4,
                "average_duration": "1-2 months"
            },
            {
                "id": "amazon",
                "name": "Amazon",
                "industry": "Technology",
                "size": "Large",
                "location": "Seattle, WA",
                "description": "E-commerce and cloud computing giant with diverse technology offerings",
                "website": "https://amazon.com",
                "logo_url": "https://example.com/logos/amazon.png",
                "difficulty": "hard",
                "interview_rounds": 5,
                "average_duration": "2-3 months"
            },
            {
                "id": "meta",
                "name": "Meta",
                "industry": "Technology",
                "size": "Large",
                "location": "Menlo Park, CA",
                "description": "Social media and technology company focused on connecting people",
                "website": "https://meta.com",
                "logo_url": "https://example.com/logos/meta.png",
                "difficulty": "hard",
                "interview_rounds": 4,
                "average_duration": "1-2 months"
            },
            {
                "id": "apple",
                "name": "Apple",
                "industry": "Technology",
                "size": "Large",
                "location": "Cupertino, CA",
                "description": "Consumer electronics and software company known for innovation",
                "website": "https://apple.com",
                "logo_url": "https://example.com/logos/apple.png",
                "difficulty": "hard",
                "interview_rounds": 6,
                "average_duration": "2-3 months"
            },
            {
                "id": "netflix",
                "name": "Netflix",
                "industry": "Entertainment",
                "size": "Large",
                "location": "Los Gatos, CA",
                "description": "Streaming entertainment service with global reach",
                "website": "https://netflix.com",
                "logo_url": "https://example.com/logos/netflix.png",
                "difficulty": "hard",
                "interview_rounds": 4,
                "average_duration": "1-2 months"
            },
            {
                "id": "uber",
                "name": "Uber",
                "industry": "Transportation",
                "size": "Large",
                "location": "San Francisco, CA",
                "description": "Ride-sharing and food delivery platform",
                "website": "https://uber.com",
                "logo_url": "https://example.com/logos/uber.png",
                "difficulty": "medium",
                "interview_rounds": 4,
                "average_duration": "1-2 months"
            },
            {
                "id": "airbnb",
                "name": "Airbnb",
                "industry": "Hospitality",
                "size": "Large",
                "location": "San Francisco, CA",
                "description": "Online marketplace for lodging and experiences",
                "website": "https://airbnb.com",
                "logo_url": "https://example.com/logos/airbnb.png",
                "difficulty": "medium",
                "interview_rounds": 4,
                "average_duration": "1-2 months"
            },
            {
                "id": "stripe",
                "name": "Stripe",
                "industry": "Fintech",
                "size": "Large",
                "location": "San Francisco, CA",
                "description": "Payment processing platform for internet businesses",
                "website": "https://stripe.com",
                "logo_url": "https://example.com/logos/stripe.png",
                "difficulty": "hard",
                "interview_rounds": 5,
                "average_duration": "2-3 months"
            },
            {
                "id": "spotify",
                "name": "Spotify",
                "industry": "Entertainment",
                "size": "Large",
                "location": "Stockholm, Sweden",
                "description": "Music streaming platform with global user base",
                "website": "https://spotify.com",
                "logo_url": "https://example.com/logos/spotify.png",
                "difficulty": "medium",
                "interview_rounds": 4,
                "average_duration": "1-2 months"
            }
        ]
        
        return {
            "companies": companies,
            "total": len(companies),
            "message": "Successfully retrieved company list"
        }
        
    except Exception as e:
        logger.error(f"Error getting companies: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get companies")


@router.get("/{company_id}")
async def get_company_details(company_id: str):
    """Get detailed information about a specific company."""
    try:
        # Mock company details
        company_details = {
            "google": {
                "id": "google",
                "name": "Google",
                "industry": "Technology",
                "size": "Large",
                "location": "Mountain View, CA",
                "description": "Leading technology company specializing in search, cloud computing, and AI",
                "website": "https://google.com",
                "logo_url": "https://example.com/logos/google.png",
                "founded": 1998,
                "employees": "150,000+",
                "revenue": "$307.4B (2023)",
                "difficulty": "hard",
                "interview_rounds": 5,
                "average_duration": "2-3 months",
                "technologies": ["Python", "Java", "C++", "Go", "JavaScript", "Kubernetes", "TensorFlow"],
                "benefits": ["Competitive salary", "Health insurance", "401k matching", "Free meals", "Gym membership"],
                "culture": "Innovation-focused, collaborative, data-driven",
                "remote_policy": "Hybrid (3 days office, 2 days remote)"
            },
            "microsoft": {
                "id": "microsoft",
                "name": "Microsoft",
                "industry": "Technology",
                "size": "Large",
                "location": "Redmond, WA",
                "description": "Global technology company focused on software, cloud services, and hardware",
                "website": "https://microsoft.com",
                "logo_url": "https://example.com/logos/microsoft.png",
                "founded": 1975,
                "employees": "220,000+",
                "revenue": "$211.9B (2023)",
                "difficulty": "hard",
                "interview_rounds": 4,
                "average_duration": "1-2 months",
                "technologies": ["C#", ".NET", "Azure", "TypeScript", "React", "Power BI"],
                "benefits": ["Competitive salary", "Health insurance", "Stock options", "Professional development"],
                "culture": "Growth mindset, inclusive, customer-focused",
                "remote_policy": "Flexible (team-dependent)"
            },
            "amazon": {
                "id": "amazon",
                "name": "Amazon",
                "industry": "Technology",
                "size": "Large",
                "location": "Seattle, WA",
                "description": "E-commerce and cloud computing giant with diverse technology offerings",
                "website": "https://amazon.com",
                "logo_url": "https://example.com/logos/amazon.png",
                "founded": 1994,
                "employees": "1.5M+",
                "revenue": "$574.8B (2023)",
                "difficulty": "hard",
                "interview_rounds": 5,
                "average_duration": "2-3 months",
                "technologies": ["Java", "Python", "AWS", "React", "Node.js", "DynamoDB"],
                "benefits": ["Competitive salary", "Health insurance", "401k matching", "Stock options"],
                "culture": "Customer-obsessed, ownership, bias for action",
                "remote_policy": "Hybrid (varies by team)"
            }
        }
        
        if company_id not in company_details:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return company_details[company_id]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting company details: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get company details")


@router.get("/{company_id}/interview-flow")
async def get_company_interview_flow(company_id: str):
    """Get detailed interview flow for a specific company."""
    try:
        # Mock interview flows
        interview_flows = {
            "google": {
                "company_id": "google",
                "company_name": "Google",
                "stages": [
                    {
                        "stage": 1,
                        "name": "Phone Screen",
                        "duration": "45 minutes",
                        "type": "Technical",
                        "description": "Initial technical screening with a Google engineer",
                        "topics": ["Algorithms", "Data Structures", "System Design basics"],
                        "tips": [
                            "Practice coding on a whiteboard or shared editor",
                            "Think out loud while solving problems",
                            "Ask clarifying questions before starting"
                        ]
                    },
                    {
                        "stage": 2,
                        "name": "Onsite Interviews",
                        "duration": "Full day (4-5 interviews)",
                        "type": "Technical + Behavioral",
                        "description": "Multiple rounds of technical and behavioral interviews",
                        "topics": [
                            "Algorithms and Data Structures",
                            "System Design",
                            "Behavioral Questions",
                            "Coding Problems"
                        ],
                        "tips": [
                            "Prepare for both technical and behavioral questions",
                            "Practice system design problems",
                            "Have specific examples ready for behavioral questions"
                        ]
                    },
                    {
                        "stage": 3,
                        "name": "Hiring Committee Review",
                        "duration": "1-2 weeks",
                        "type": "Decision",
                        "description": "Committee reviews all interview feedback and makes decision",
                        "topics": ["Interview feedback review", "Team matching"],
                        "tips": ["Be patient during this stage", "Follow up with recruiter if needed"]
                    }
                ],
                "typical_duration": "2-3 months",
                "difficulty": "hard",
                "tips": [
                    "Practice coding problems on platforms like LeetCode",
                    "Study system design concepts thoroughly",
                    "Prepare STAR method for behavioral questions",
                    "Research Google's products and culture",
                    "Practice with mock interviews"
                ],
                "sample_questions": [
                    "Design a URL shortening service",
                    "Implement a rate limiter",
                    "Tell me about a time you had to learn something quickly",
                    "How would you design Google Maps?",
                    "Reverse a linked list"
                ]
            },
            "microsoft": {
                "company_id": "microsoft",
                "company_name": "Microsoft",
                "stages": [
                    {
                        "stage": 1,
                        "name": "Phone Screen",
                        "duration": "45 minutes",
                        "type": "Technical",
                        "description": "Initial technical screening",
                        "topics": ["Algorithms", "Coding", "Basic system design"],
                        "tips": ["Practice coding in your preferred language", "Be ready to explain your thought process"]
                    },
                    {
                        "stage": 2,
                        "name": "Onsite Interviews",
                        "duration": "Full day (4-5 interviews)",
                        "type": "Technical + Behavioral",
                        "description": "Multiple rounds covering technical and behavioral aspects",
                        "topics": ["Coding", "System Design", "Behavioral", "Team fit"],
                        "tips": ["Prepare for both technical and behavioral questions", "Research Microsoft's products"]
                    }
                ],
                "typical_duration": "1-2 months",
                "difficulty": "hard",
                "tips": [
                    "Practice coding problems",
                    "Study system design",
                    "Prepare behavioral questions",
                    "Research Microsoft's culture and values"
                ],
                "sample_questions": [
                    "Design a chat application",
                    "Implement a cache",
                    "Tell me about a challenging project",
                    "How would you handle conflicting requirements?"
                ]
            },
            "amazon": {
                "company_id": "amazon",
                "company_name": "Amazon",
                "stages": [
                    {
                        "stage": 1,
                        "name": "Online Assessment",
                        "duration": "90 minutes",
                        "type": "Technical",
                        "description": "Online coding assessment with multiple problems",
                        "topics": ["Algorithms", "Data Structures", "Coding"],
                        "tips": ["Practice time management", "Test your code thoroughly"]
                    },
                    {
                        "stage": 2,
                        "name": "Phone Screen",
                        "duration": "45 minutes",
                        "type": "Technical",
                        "description": "Technical phone interview",
                        "topics": ["Coding", "System Design basics"],
                        "tips": ["Practice coding on a shared editor", "Think out loud"]
                    },
                    {
                        "stage": 3,
                        "name": "Onsite Interviews",
                        "duration": "Full day (4-5 interviews)",
                        "type": "Technical + Behavioral",
                        "description": "Multiple rounds including behavioral and technical",
                        "topics": ["Coding", "System Design", "Leadership Principles"],
                        "tips": ["Study Amazon's Leadership Principles", "Prepare STAR method answers"]
                    }
                ],
                "typical_duration": "2-3 months",
                "difficulty": "hard",
                "tips": [
                    "Study Amazon's 14 Leadership Principles",
                    "Practice coding problems",
                    "Prepare behavioral questions using STAR method",
                    "Research Amazon's products and services"
                ],
                "sample_questions": [
                    "Tell me about a time you disagreed with your manager",
                    "Design a recommendation system",
                    "Implement a queue using stacks",
                    "How would you handle a difficult customer?"
                ]
            }
        }
        
        if company_id not in interview_flows:
            raise HTTPException(status_code=404, detail="Company interview flow not found")
        
        return interview_flows[company_id]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting interview flow: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get interview flow")


@router.get("/{company_id}/questions")
async def get_company_questions(company_id: str, category: Optional[str] = None):
    """Get sample interview questions for a specific company."""
    try:
        # Mock questions by company and category
        questions = {
            "google": {
                "technical": [
                    "Design a URL shortening service",
                    "Implement a rate limiter",
                    "How would you design Google Maps?",
                    "Reverse a linked list",
                    "Find the longest palindromic substring"
                ],
                "behavioral": [
                    "Tell me about a time you had to learn something quickly",
                    "Describe a challenging project you worked on",
                    "How do you handle conflicting priorities?",
                    "Tell me about a time you failed and what you learned"
                ],
                "system_design": [
                    "Design a chat application",
                    "Design a recommendation system",
                    "Design a search engine",
                    "Design a distributed cache"
                ]
            },
            "microsoft": {
                "technical": [
                    "Design a chat application",
                    "Implement a cache",
                    "Reverse a string",
                    "Find the missing number in an array",
                    "Design a parking lot system"
                ],
                "behavioral": [
                    "Tell me about a challenging project",
                    "How would you handle conflicting requirements?",
                    "Describe a time you had to work with a difficult team member",
                    "Tell me about a time you had to make a difficult decision"
                ],
                "system_design": [
                    "Design a file sharing system",
                    "Design a notification service",
                    "Design a load balancer",
                    "Design a database"
                ]
            },
            "amazon": {
                "technical": [
                    "Design a recommendation system",
                    "Implement a queue using stacks",
                    "Find the longest common subsequence",
                    "Design a parking lot system",
                    "Implement a cache with LRU eviction"
                ],
                "behavioral": [
                    "Tell me about a time you disagreed with your manager",
                    "How would you handle a difficult customer?",
                    "Describe a time you had to make a decision with incomplete information",
                    "Tell me about a time you had to learn something quickly"
                ],
                "system_design": [
                    "Design an e-commerce system",
                    "Design a notification service",
                    "Design a recommendation system",
                    "Design a distributed cache"
                ]
            }
        }
        
        if company_id not in questions:
            raise HTTPException(status_code=404, detail="Company questions not found")
        
        company_questions = questions[company_id]
        
        if category and category in company_questions:
            return {
                "company_id": company_id,
                "category": category,
                "questions": company_questions[category]
            }
        
        return {
            "company_id": company_id,
            "categories": list(company_questions.keys()),
            "questions": company_questions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting company questions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get company questions")


@router.get("/search")
async def search_companies(
    query: str = Query(..., description="Search query"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level")
):
    """Search companies by name, industry, or other criteria."""
    try:
        # Mock search functionality
        all_companies = [
            {"id": "google", "name": "Google", "industry": "Technology", "difficulty": "hard"},
            {"id": "microsoft", "name": "Microsoft", "industry": "Technology", "difficulty": "hard"},
            {"id": "amazon", "name": "Amazon", "industry": "Technology", "difficulty": "hard"},
            {"id": "netflix", "name": "Netflix", "industry": "Entertainment", "difficulty": "hard"},
            {"id": "uber", "name": "Uber", "industry": "Transportation", "difficulty": "medium"},
            {"id": "stripe", "name": "Stripe", "industry": "Fintech", "difficulty": "hard"}
        ]
        
        # Simple search implementation
        results = []
        query_lower = query.lower()
        
        for company in all_companies:
            if (query_lower in company["name"].lower() or 
                query_lower in company["industry"].lower()):
                
                # Apply filters
                if industry and company["industry"].lower() != industry.lower():
                    continue
                if difficulty and company["difficulty"] != difficulty:
                    continue
                
                results.append(company)
        
        return {
            "query": query,
            "filters": {"industry": industry, "difficulty": difficulty},
            "results": results,
            "total": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error searching companies: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search companies") 