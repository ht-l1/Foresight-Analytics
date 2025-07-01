from pydantic_settings import BaseSettings
from typing import Optional

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

    class Config:
        env_file = ".env"

settings = Settings()