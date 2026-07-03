from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MyApp"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int 
    REFRESH_TOKEN_EXPIRE_MONTHS: int 
    redis_url: str


    class Config:
        env_file = ".env"

settings = Settings()