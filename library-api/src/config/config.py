from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    APP_NAME: str = "Library API"
    APP_VERSION: str = "1.0.0"
    APP_URL: str = "127.0.0.1"
    APP_PORT: int = 8000
    APP_DEBUG: bool = False
    DATABASE_URL: str = ""
    AUTH_USERNAME: str = ""
    AUTH_PASSWORD: str = ""

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '../..', '.env')
        extra = 'allow'


settings = Settings()
