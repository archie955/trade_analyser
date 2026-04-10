from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    secret_key: str
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    algorithm: str
    access_token_expire_minutes: int
    model_config = ConfigDict(env_file=".env.dev")

settings = Settings()