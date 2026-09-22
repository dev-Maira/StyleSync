from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Existing variables
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # New Gemini Key
    GOOGLE_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()