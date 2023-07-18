import logging
from functools import lru_cache
from pathlib import Path

from pydantic.v1 import BaseSettings


class ApplicationSettings(BaseSettings):
    class Config:
        env_file = Path(__file__).parent.parent / ".env"

    TG_USER: str
    TG_PASS: str

    BINANCE_API_KEY: str
    BINANCE_SECRET: str


def log_settings(_settings: ApplicationSettings, logger: logging.Logger) -> None:
    for k, v in sorted(_settings.dict().items(), key=lambda x: x[0]):
        logger.info(f"{k.upper()}: {v}")


@lru_cache()
def get_app_settings() -> ApplicationSettings:
    return ApplicationSettings()
