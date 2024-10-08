import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    PROJECT_NAME: str = "Sales Manager API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/salesmanager?uuidRepresentation=standard&authSource=admin")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "salesmanager")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_HOSTS: list = ["*"]
    SAMPLE_DATA_FILE: str = os.getenv("SAMPLE_DATA_FILE", "sample_data.json")
    
    # AI model settings
    DEFAULT_AI_MODEL: str = os.getenv("DEFAULT_AI_MODEL", "openrouter/anthropic/claude-3.5-sonnet")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")

    class Config:
        case_sensitive = True

settings = Settings()
