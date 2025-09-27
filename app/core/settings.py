from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "local"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 120

    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
