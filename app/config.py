from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # GitHub App
    github_app_id: int
    github_app_private_key: str
    github_webhook_secret: str
    github_client_id: str
    github_client_secret: str

    # Database
    database_url: str

    # Redis
    redis_url: str

    # App
    base_url: str
    frontend_url: str
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()
