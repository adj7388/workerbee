import logging
import sys


def configure_logging(level=logging.INFO):
    root_logger = logging.getLogger()
    root_logger.info("root_logger.info: setting up logging")
    print("print: setting up logging")
    if root_logger.hasHandlers():
        # already configured
        return

    root_logger.setLevel(level)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | PID %(process)d | %(name)s: %(message)s"
        )
    )
    root_logger.addHandler(handler)
