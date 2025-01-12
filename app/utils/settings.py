from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    DB_URL: str = config("DB_URL")
    PORT: int = config("PORT", cast=int)


settings = Settings()
