import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    NUM_REQUIRED_LETTERS = 1
    NUM_ALLOWED_LETTERS = 6
    MIN_WORD_LENGTH = 4
    SECRET_KEY = os.environ.get("SECRETBEEKEY")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
