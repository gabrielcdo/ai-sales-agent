from typing import Optional

from pydantic_settings import BaseSettings
from app.core.singleton import singleton


@singleton
class Settings(BaseSettings):
    # API

    api_name: str = "ai_agent"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int
    prefix: str = "/api/ai_agent"
    autoreload: bool = True

    environment: str = "local"

    openai_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
