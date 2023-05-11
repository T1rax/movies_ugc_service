from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class AppSettings(BaseSettings):
    project_host: str = Field(env="PROJECT_HOST", default="0.0.0.0")
    project_port: int = Field(env="PROJECT_PORT", default=8000)

    log_format: str = Field(env="LOG_FORMAT", default="INFO")

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


settings = AppSettings()
