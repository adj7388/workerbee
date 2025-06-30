import os
from dataclasses import dataclass
from .constants import Consts


@dataclass(frozen=True)
class Config:
    NUM_REQUIRED_LETTERS = 1
    NUM_ALLOWED_LETTERS = 6
    MIN_WORD_LENGTH = 4
    SECRET_KEY = os.environ.get("SECRETBEEKEY")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    PROFILING = (
        True
        if os.environ.get(Consts.BEEPROFILE, "").lower() == Consts.BEEPROFILE.lower()
        else False
    )
