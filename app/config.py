from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # GitHub App
    github_app_id: int
    github_app_private_key_path: str = "./private-key.pem"
    github_app_private_key: str = ""
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

    @field_validator("github_app_private_key", mode="before")
    @classmethod
    def load_private_key(cls, v, info):
        if not v:
            path = Path("./private-key.pem")
            if path.exists():
                return path.read_text()
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
