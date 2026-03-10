from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Land Leasing API'
    debug: bool = False

    secret_key: str = Field(..., min_length=32)
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30
    issuer: str = 'land-leasing-api'
    audience: str = 'land-leasing-users'

    database_url: str = 'sqlite:///./land_leasing.db'

    allowed_origins: list[str] = ['http://localhost:3000']
    max_login_attempts_per_minute: int = 10


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
