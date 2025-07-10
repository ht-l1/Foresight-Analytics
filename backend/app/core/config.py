from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

# Load .env manually
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # database 
    database_url: str
    neon_database_url: Optional[str] = None

    # redis
    redis_url: str
    upstash_redis_url: Optional[str] = None

    # API Keys
    fmp_api_key: str

    # security
    secret_key: str
    algorithm: str="HS256"
    access_token_expire_minutes: int=30

    # app
    app_name: str = "Finance Analytics Platform"
    environment: str = "development"

    # FMP API Configuration
    fmp_base_url: str = "https://financialmodelingprep.com/stable"
    fmp_rate_limit_delay: int = 1  # seconds between requests for free tier
    
    # Data fetch limits (free tier constraints)
    fmp_max_companies: int = 5  # FAANG companies
    fmp_max_periods: int = 5
    fmp_max_articles: int = 20  # articles per request

    # FAANG Symbol
    FAANG_SYMBOLS: list[str] = ["META", "AAPL", "AMZN", "NFLX", "GOOGL"]

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()