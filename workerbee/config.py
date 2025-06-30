from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    NUM_REQUIRED_LETTERS = 1
    NUM_ALLOWED_LETTERS = 6
    MIN_WORD_LENGTH = 4
