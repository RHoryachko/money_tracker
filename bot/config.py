from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    bot_token: str
    api_url: str = "http://backend:8000"
    admin_chat_id: Optional[int] = None
    
    class Config:
        env_file = ".env"

settings = Settings()