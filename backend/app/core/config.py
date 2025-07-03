from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

# Load .env manually
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # database 
    DATABASE_URL: str
    NEON_DATABASE_URL: Optional[str] = None

    # redis
    REDIS_URL: str
    UPSTASH_REDIS_URL: Optional[str] = None

    # API Keys
    FMP_API_KEY: str

    # security
    SECRET_KEY: str
    ALGORITHM: str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int=30

    # app
    app_name: str = "Finance Analytics Platform"
    ENVIRONMENT: str = "development"

    # FMP API Configuration
    FMP_API_KEY: str = ""
    FMP_BASE_URL: str = "https://financialmodelingprep.com/api/v3"
    FMP_RATE_LIMIT_DELAY: int = 1  # seconds between requests for free tier
    
    # Data fetch limits (free tier constraints)
    FMP_MAX_COMPANIES: int = 5  # FAANG companies
    FMP_MAX_PERIODS: int = 20   # quarters per company
    FMP_MAX_ARTICLES: int = 20  # articles per request

    class Config:
        env_file = ".env"

settings = Settings()