import logging
import os


class Config:
    NUM_REQUIRED_LETTERS: int = 1
    NUM_ALLOWED_LETTERS: int = 6
    MIN_WORD_LENGTH: int = 4
    SECRET_KEY: str | None = os.environ.get("SECRETBEEKEY")

    LOG_LEVEL: int = logging.WARNING
    DEBUG: bool = False
    MAX_CACHE_SIZE: int = 10


class DevConfig(Config):
    LOG_LEVEL: int = logging.DEBUG
    DEBUG: bool = True


class ProdConfig(Config):
    LOG_LEVEL: int = logging.INFO
    DEBUG: bool = False
    MAX_CACHE_SIZE: int = 30
