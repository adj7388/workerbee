import logging
import os
import pathlib

_logger = logging.getLogger(__name__)


def _get_commit_hash(path_str: str) -> str:
    commit = "unknown"
    path = pathlib.Path(path_str)
    if path.exists():
        commit = path.read_text().strip()
    return commit


class Config:
    _COMMIT_HASH_FILE = "workerbee/commit.txt"
    COMMIT_HASH = _get_commit_hash(_COMMIT_HASH_FILE)
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
