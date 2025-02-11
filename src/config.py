from typing import Any

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn

    APP_VERSION: str = "1.0"


settings: Config = Config()

app_configs: dict[str, Any] = {
    "title": "Invest CRM API",
}
