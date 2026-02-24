from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Restaurant POS API"
    DEBUG: bool = False

    LOG_LEVEL: str = "INFO"  # DEBUG / INFO / WARNING / ERROR
    LOG_FORMAT: str = "text"  # text (позже можно json)

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_NAME: str = "restaurant"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()