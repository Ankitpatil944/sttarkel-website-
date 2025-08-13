"""
Main FastAPI application entry point for SttarkelTool backend.
Configures routes, middleware, and application settings.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from app.config import settings
from app.routes import auth, assessment, interview_ai, dashboard, company
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("🚀 Starting SttarkelTool Backend...")
    await init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down SttarkelTool Backend...")


# Create FastAPI app instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A comprehensive job preparation platform with AI-driven assessments and interviews",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(assessment.router, prefix="/assessment", tags=["Assessments"])
app.include_router(interview_ai.router, prefix="/interview", tags=["AI Interviews"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard & Analytics"])
app.include_router(company.router, prefix="/company", tags=["Company Data"])


@app.get("/")
async def root():
    """Root endpoint with application info."""
    return {
        "message": "Welcome to SttarkelTool Backend",
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "services": {
            "database": "connected",
            "tavus_api": "available" if settings.tavus_api_key else "not_configured"
        }
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    ) 