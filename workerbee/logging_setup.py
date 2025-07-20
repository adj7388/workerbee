import logging
import sys


def configure_logging():
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        # already configured
        return

    root_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | PID %(process)d | %(name)s: %(message)s"
        )
    )
    root_logger.addHandler(handler)
