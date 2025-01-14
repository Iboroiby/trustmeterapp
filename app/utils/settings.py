from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    DB_URL: str = config("DB_URL")
    PORT: int = config("PORT", cast=int)
    JWT_SECRET: str = config("JWT_SECRET")
    JWT_ALGORITHM: str = config("JWT_ALGORITHM")


settings = Settings()
