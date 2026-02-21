from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SIGPS API"
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    JWT_SECRET: str
    JWT_EXPIRES_MINUTES: int = 120

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()
