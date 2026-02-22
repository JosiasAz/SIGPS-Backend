from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "dev"
    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 1 dia

    ML_MODEL_DIR: str = "./data/models"
    ML_MODEL_NAME: str = "model.pkl"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()