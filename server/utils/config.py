from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    secret_key: str
    postgres_hostname: str
    postgres_port: int
    postgres_password: str
    postgres_name: str
    postgres_username: str
    algorithm: str
    access_token_expire_minutes: int

    # model_config = ConfigDict(case_sensitive=False)
    model_config = ConfigDict(env_file=".env.dev")


settings = Settings()
