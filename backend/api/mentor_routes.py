from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

router = APIRouter(prefix="/mentors", tags=["mentors"])

# In-memory storage for demo purposes (replace with database in production)
mentor_applications = []
verified_mentors = []
mentor_sessions = []

# Sample verified mentors data
sample_verified_mentors = [
    {
        "id": 1,
        "name": "Dr. Priya Sharma",
        "displayName": "priya_sharma_ml",
        "role": "Senior Software Engineer",
        "company": "TCS",
        "experience": "8+ years",
        "category": "Python",
        "subcategory": "Machine Learning & AI",
        "rating": 4.9,
        "sessions": 150,
        "hourlyRate": 2500,
        "location": "Bangalore",
        "image": "/Images/Sttarkel_Student.png",
        "expertise": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"],
        "availability": "Weekdays 6-9 PM",
        "isVerified": True,
        "verificationDate": "2024-01-15",
        "responseTime": "< 2 hours",
        "successRate": "98%",
        "bio": "Experienced ML engineer with 8+ years in developing scalable AI solutions. Passionate about mentoring and helping others grow in the field of machine learning.",
        "email": "priya.sharma@example.com",
        "phone": "+91 98765 43210",
        "linkedinUrl": "https://linkedin.com/in/priya-sharma",
        "githubUrl": "https://github.com/priya-sharma",
        "portfolioUrl": "https://priyasharma.dev",
        "education": "Master's Degree",
        "certifications": ["AWS Machine Learning Specialty", "Google Cloud ML Engineer"]
    },
    {
        "id": 2,
        "name": "Rajesh Kumar",
        "displayName": "rajesh_kumar_dev",
        "role": "Product Manager",
        "company": "Infosys",
        "experience": "6+ years",
        "category": "JavaScript",
        "subcategory": "Full Stack Development",
        "rating": 4.8,
        "sessions": 120,
        "hourlyRate": 2000,
        "location": "Mumbai",
        "image": "/Images/Sttarkel_Student.png",
        "expertise": ["JavaScript", "React", "Node.js", "MongoDB", "AWS"],
        "availability": "Weekends 10 AM-6 PM",
        "isVerified": True,
        "verificationDate": "2024-02-20",
        "responseTime": "< 4 hours",
        "successRate": "95%",
        "bio": "Product Manager with 6+ years of experience in building scalable web applications. Expert in modern JavaScript frameworks and cloud technologies.",
        "email": "rajesh.kumar@example.com",
        "phone": "+91 98765 43211",
        "linkedinUrl": "https://linkedin.com/in/rajesh-kumar",
        "githubUrl": "https://github.com/rajesh-kumar",
        "portfolioUrl": "https://rajeshkumar.dev",
        "education": "Bachelor's Degree",
        "certifications": ["AWS Solutions Architect", "MongoDB Developer"]
    },
    {
        "id": 3,
        "name": "Anjali Patel",
        "displayName": "anjali_patel_ds",
        "role": "Data Scientist",
        "company": "Wipro",
        "experience": "5+ years",
        "category": "Data Science",
        "subcategory": "Machine Learning",
        "rating": 4.9,
        "sessions": 95,
        "hourlyRate": 2200,
        "location": "Hyderabad",
        "image": "/Images/Sttarkel_Student.png",
        "expertise": ["Python", "R", "SQL", "Scikit-learn", "Pandas"],
        "availability": "Weekdays 7-10 PM",
        "isVerified": True,
        "verificationDate": "2024-03-10",
        "responseTime": "< 1 hour",
        "successRate": "99%",
        "bio": "Data Scientist with expertise in statistical analysis and machine learning. Passionate about helping students understand complex data science concepts.",
        "email": "anjali.patel@example.com",
        "phone": "+91 98765 43212",
        "linkedinUrl": "https://linkedin.com/in/anjali-patel",
        "githubUrl": "https://github.com/anjali-patel",
        "portfolioUrl": "https://anjalipatel.dev",
        "education": "Master's Degree",
        "certifications": ["IBM Data Science Professional", "Microsoft Azure Data Scientist"]
    }
]

# Initialize with sample data
verified_mentors.extend(sample_verified_mentors)

@router.post("/apply")
async def apply_as_mentor(
    background_tasks: BackgroundTasks,
    firstName: str = Form(...),
    lastName: str = Form(...),
    displayName: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    bio: str = Form(...),
    currentRole: str = Form(...),
    company: str = Form(...),
    experience: str = Form(...),
    expertise: str = Form(...),  # JSON string
    education: Optional[str] = Form(None),
    certifications: Optional[str] = Form(None),  # JSON string
    linkedinUrl: Optional[str] = Form(None),
    githubUrl: Optional[str] = Form(None),
    portfolioUrl: Optional[str] = Form(None),
    password: str = Form(...),
    agreeToTerms: bool = Form(...),
    agreeToPrivacy: bool = Form(...),
    agreeToMentorGuidelines: bool = Form(...),
    resume: Optional[UploadFile] = File(None)
):
    """
    Submit a mentor application
    """
    try:
        # Validate required fields
        if not all([firstName, lastName, displayName, email, bio, currentRole, company, experience, password]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        if not all([agreeToTerms, agreeToPrivacy, agreeToMentorGuidelines]):
            raise HTTPException(status_code=400, detail="All agreements must be accepted")
        
        # Check if email already exists
        if any(mentor["email"] == email for mentor in verified_mentors):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if display name already exists
        if any(mentor["displayName"] == displayName for mentor in verified_mentors):
            raise HTTPException(status_code=400, detail="Display name already taken")
        
        # Parse expertise and certifications
        try:
            expertise_list = json.loads(expertise) if expertise else []
            certifications_list = json.loads(certifications) if certifications else []
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format for expertise or certifications")
        
        # Handle resume upload
        resume_path = None
        if resume:
            # Create uploads directory if it doesn't exist
            upload_dir = Path("uploads/resumes")
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            # Save file with unique name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{displayName}_{timestamp}_{resume.filename}"
            file_path = upload_dir / filename
            
            with open(file_path, "wb") as buffer:
                content = await resume.read()
                buffer.write(content)
            resume_path = str(file_path)
        
        # Create application
        application = {
            "id": len(mentor_applications) + 1,
            "firstName": firstName,
            "lastName": lastName,
            "displayName": displayName,
            "email": email,
            "phone": phone,
            "location": location,
            "bio": bio,
            "currentRole": currentRole,
            "company": company,
            "experience": experience,
            "expertise": expertise_list,
            "education": education,
            "certifications": certifications_list,
            "linkedinUrl": linkedinUrl,
            "githubUrl": githubUrl,
            "portfolioUrl": portfolioUrl,
            "resumePath": resume_path,
            "status": "pending",  # pending, approved, rejected
            "submittedAt": datetime.now().isoformat(),
            "reviewedAt": None,
            "reviewerNotes": None
        }
        
        mentor_applications.append(application)
        
        # In a real application, you would:
        # 1. Hash the password and store securely
        # 2. Send confirmation email
        # 3. Notify admin team for review
        # 4. Store in database
        
        background_tasks.add_task(send_application_confirmation_email, email, displayName)
        
        return {
            "message": "Application submitted successfully",
            "applicationId": application["id"],
            "status": "pending",
            "estimatedReviewTime": "3-5 business days"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/list")
async def get_mentors(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    search: Optional[str] = None,
    verified_only: bool = False,
    min_rating: Optional[float] = None,
    max_price: Optional[int] = None,
    location: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """
    Get list of verified mentors with filtering options
    """
    try:
        mentors = verified_mentors.copy()
        
        # Apply filters
        if verified_only:
            mentors = [m for m in mentors if m.get("isVerified", False)]
        
        if category:
            mentors = [m for m in mentors if m.get("category") == category]
        
        if subcategory:
            mentors = [m for m in mentors if m.get("subcategory") == subcategory]
        
        if search:
            search_lower = search.lower()
            mentors = [m for m in mentors if 
                      search_lower in m.get("name", "").lower() or
                      search_lower in m.get("role", "").lower() or
                      search_lower in m.get("company", "").lower() or
                      any(search_lower in skill.lower() for skill in m.get("expertise", []))]
        
        if min_rating:
            mentors = [m for m in mentors if m.get("rating", 0) >= min_rating]
        
        if max_price:
            mentors = [m for m in mentors if m.get("hourlyRate", 0) <= max_price]
        
        if location:
            location_lower = location.lower()
            mentors = [m for m in mentors if location_lower in m.get("location", "").lower()]
        
        # Apply pagination
        total_count = len(mentors)
        mentors = mentors[offset:offset + limit]
        
        return {
            "mentors": mentors,
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "hasMore": offset + limit < total_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{mentor_id}")
async def get_mentor_details(mentor_id: int):
    """
    Get detailed information about a specific mentor
    """
    try:
        mentor = next((m for m in verified_mentors if m["id"] == mentor_id), None)
        
        if not mentor:
            raise HTTPException(status_code=404, detail="Mentor not found")
        
        # Get mentor's session history
        mentor_sessions_list = [s for s in mentor_sessions if s["mentorId"] == mentor_id]
        
        # Calculate additional stats
        total_sessions = len(mentor_sessions_list)
        completed_sessions = len([s for s in mentor_sessions_list if s["status"] == "completed"])
        avg_session_duration = sum(s.get("duration", 60) for s in mentor_sessions_list) / len(mentor_sessions_list) if mentor_sessions_list else 0
        
        mentor_details = {
            **mentor,
            "stats": {
                "totalSessions": total_sessions,
                "completedSessions": completed_sessions,
                "completionRate": (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
                "avgSessionDuration": round(avg_session_duration, 1),
                "totalEarnings": sum(s.get("amount", 0) for s in mentor_sessions_list if s["status"] == "completed")
            },
            "recentSessions": mentor_sessions_list[-5:] if mentor_sessions_list else []
        }
        
        return mentor_details
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/categories/list")
async def get_mentor_categories():
    """
    Get list of available mentor categories and subcategories
    """
    categories = {
        "Python": [
            "Web Development (Django/Flask)",
            "Data Science & Analytics",
            "Machine Learning & AI",
            "Automation & Scripting",
            "DevOps & Infrastructure",
            "Game Development",
            "Desktop Applications",
            "API Development"
        ],
        "JavaScript": [
            "Frontend Development (React/Vue/Angular)",
            "Backend Development (Node.js)",
            "Full Stack Development",
            "Mobile Development (React Native)",
            "Game Development",
            "Desktop Applications (Electron)",
            "Testing & QA"
        ],
        "Java": [
            "Enterprise Development",
            "Android Development",
            "Spring Framework",
            "Microservices",
            "Big Data Processing",
            "Cloud Development",
            "Performance Optimization"
        ],
        "Data Science": [
            "Machine Learning",
            "Deep Learning",
            "Statistical Analysis",
            "Data Visualization",
            "Natural Language Processing",
            "Computer Vision",
            "Big Data Analytics"
        ],
        "DevOps": [
            "CI/CD Pipelines",
            "Cloud Infrastructure (AWS/Azure/GCP)",
            "Containerization (Docker/Kubernetes)",
            "Monitoring & Logging",
            "Security & Compliance",
            "Infrastructure as Code",
            "Performance Tuning"
        ],
        "Mobile Development": [
            "iOS Development (Swift)",
            "Android Development (Kotlin/Java)",
            "Cross-platform (Flutter/React Native)",
            "Mobile UI/UX Design",
            "App Store Optimization",
            "Mobile Testing",
            "Performance Optimization"
        ]
    }
    
    return {"categories": categories}

@router.get("/applications/status/{application_id}")
async def get_application_status(application_id: int):
    """
    Check the status of a mentor application
    """
    try:
        application = next((app for app in mentor_applications if app["id"] == application_id), None)
        
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        return {
            "applicationId": application["id"],
            "status": application["status"],
            "submittedAt": application["submittedAt"],
            "reviewedAt": application["reviewedAt"],
            "reviewerNotes": application["reviewerNotes"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/book-session")
async def book_mentor_session(
    mentor_id: int,
    mentee_id: int,
    session_date: str,
    session_duration: int = 60,
    session_type: str = "video_call",
    topics: str = None,  # JSON string
    notes: str = None
):
    """
    Book a session with a mentor
    """
    try:
        # Validate mentor exists
        mentor = next((m for m in verified_mentors if m["id"] == mentor_id), None)
        if not mentor:
            raise HTTPException(status_code=404, detail="Mentor not found")
        
        # Parse topics
        topics_list = json.loads(topics) if topics else []
        
        # Create session
        session = {
            "id": len(mentor_sessions) + 1,
            "mentorId": mentor_id,
            "menteeId": mentee_id,
            "sessionDate": session_date,
            "sessionDuration": session_duration,
            "sessionType": session_type,
            "topics": topics_list,
            "notes": notes,
            "status": "scheduled",  # scheduled, completed, cancelled
            "amount": mentor["hourlyRate"] * (session_duration / 60),
            "createdAt": datetime.now().isoformat()
        }
        
        mentor_sessions.append(session)
        
        return {
            "message": "Session booked successfully",
            "sessionId": session["id"],
            "amount": session["amount"],
            "sessionDate": session_date
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for topics")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Helper function for background tasks
async def send_application_confirmation_email(email: str, display_name: str):
    """
    Send confirmation email for mentor application
    """
    # In a real application, you would integrate with an email service
    print(f"Sending confirmation email to {email} for mentor application: {display_name}")
    # Example: await email_service.send_confirmation(email, display_name)
