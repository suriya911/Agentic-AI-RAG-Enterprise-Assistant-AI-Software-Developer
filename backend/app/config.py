from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Agentic AI Enterprise Assistant"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432/agentic_ai")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Weaviate
    WEAVIATE_API_KEY: Optional[str] = os.getenv("WEAVIATE_API_KEY")
    WEAVIATE_URL: str = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    
    # OAuth2
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    
    # API Integrations
    JIRA_API_TOKEN: Optional[str] = os.getenv("JIRA_API_TOKEN")
    SLACK_API_KEY: Optional[str] = os.getenv("SLACK_API_KEY")
    
    class Config:
        case_sensitive = True

settings = Settings() 