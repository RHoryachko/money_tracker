from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:////data/expenses.db"
    api_secret_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()