import logging
import os
import pathlib


class Config:
    COMMIT_HASH = (
        pathlib.Path("workerbee/commit.txt").read_text().strip()
        if pathlib.Path("workerbee/commit.txt").exists()
        else "unknown"
    )
    SECRET_KEY: str | None = os.environ.get("SECRETBEEKEY")
    NUM_REQUIRED_LETTERS: int = 1
    NUM_ALLOWED_LETTERS: int = 6
    MIN_WORD_LENGTH: int = 4

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
