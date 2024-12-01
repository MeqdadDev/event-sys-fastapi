from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str  # Postgres connection URL
    SECRET_KEY: str  # The secret key for JWT signing
    ALGORITHM: str  # The algorithm for JWT signing
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        # to read values from a .env file in the root directory.
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
