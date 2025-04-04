from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:////data/expenses.db"
    
    class Config:
        env_file = ".env"

settings = Settings()