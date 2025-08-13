"""
Configuration settings for SttarkelTool backend.
Handles environment variables, API keys, and application settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    app_name: str = "SttarkelTool Backend"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database settings
    database_url: str = "sqlite:///./sttarkel.db"
    
    # API Keys
    tavus_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    judge0_api_key: Optional[str] = None
    
    # Tavus CVI settings
    tavus_base_url: str = "https://api.tavus.com"
    tavus_timeout: int = 30
    
    # File upload settings
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_audio_formats: list = [".mp3", ".wav", ".m4a", ".ogg"]
    allowed_video_formats: list = [".mp4", ".avi", ".mov", ".webm"]
    
    # Assessment settings
    mcq_time_limit: int = 300  # 5 minutes
    coding_time_limit: int = 1800  # 30 minutes
    aptitude_time_limit: int = 600  # 10 minutes
    
    # AI Interview settings
    interview_session_duration: int = 1800  # 30 minutes
    max_questions_per_session: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings 