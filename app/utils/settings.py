from pydantic_settings import BaseSettings
from decouple import config
import os

class Settings(BaseSettings):
    PORT: int = config("PORT", cast=int)

    """Database Settings"""
    DB_URL: str = config("DB_URL")

    """JWT Settings"""
    JWT_SECRET: str = config("JWT_SECRET")
    JWT_ALGORITHM: str = config("JWT_ALGORITHM")

    """Email Settings"""
    MAIL_USERNAME: str = config("MAIL_USERNAME")
    MAIL_PASSWORD: str = config("MAIL_USERNAME")
    MAIL_FROM: str = config("MAIL_USERNAME")
    MAIL_PORT: int = config("MAIL_PORT", cast=int)
    MAIL_SERVER: str = config("MAIL_SERVER")



settings = Settings()