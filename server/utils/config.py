from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os
from dotenv import load_dotenv

load_dotenv(".env.dev")
TEST = os.getenv("TEST")


class Settings(BaseSettings):
    secret_key: str
    postgres_hostname: str
    postgres_port: int
    postgres_password: str
    postgres_name: str
    postgres_username: str
    algorithm: str
    test: bool
    access_token_expire_minutes: int

    if TEST:
        model_config = ConfigDict(env_file=".env.test")
    else:
        model_config = ConfigDict(case_sensitive=False)


settings = Settings()
