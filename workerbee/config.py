import logging
import os


class Config:
    NUM_REQUIRED_LETTERS = 1
    NUM_ALLOWED_LETTERS = 6
    MIN_WORD_LENGTH = 4
    SECRET_KEY = os.environ.get("SECRETBEEKEY")

    LOG_LEVEL = logging.WARNING
    DEBUG = False


class DevConfig(Config):
    LOG_LEVEL = logging.DEBUG
    DEBUG = True


class ProdConfig(Config):
    LOG_LEVEL = logging.INFO
    DEBUG = False
