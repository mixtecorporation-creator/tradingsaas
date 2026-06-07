from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./trading.db"
    database_url_sync: str = "sqlite:///./trading.db"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    storage_endpoint: str = "http://localhost:9000"
    storage_access_key: str = "minioadmin"
    storage_secret_key: str = "minioadmin"
    storage_bucket: str = "trading-screenshots"
    storage_region: str = "us-east-1"

    market_data_provider: str = "twelvedata"
    market_data_api_key: Optional[str] = None

    ai_provider: str = "openai"
    ai_api_key: Optional[str] = None
    ai_model: str = "gpt-4o-mini"

    frontend_url: str = "http://localhost:3000"
    cors_origins: list[str] = ["http://localhost:3000"]

    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None

    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/1"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
