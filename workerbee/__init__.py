import flask
import logging
import os

from dataclasses import asdict
from datetime import datetime

from .cache import init_caches
from .config import Config, DevConfig, ProdConfig
from .constants import Consts
from .dictionaries import Dictionaries
from .views import init_routes
from .wordlists import WordLists, load_word_lists
from .logging_setup import configure_logging

_logger = logging.getLogger(__name__)


def create_app(config_class=DevConfig) -> flask.Flask | None:
    config_name = os.getenv("FLASK_CONFIG", "Config")
    config_class = {
        "Config": Config,
        "DevConfig": DevConfig,
        "ProdConfig": ProdConfig,
    }.get(config_name, "Config")

    configure_logging(level=config_class.LOG_LEVEL)

    _logger.info(f"create_app configuring with {config_class.__name__} class")

    app = flask.Flask(__name__)
    app.config.from_object(config_class)

    # inject consts into Jinja for templates
    app.jinja_env.globals.update(**asdict(Consts()))
    app.jinja_env.globals.update(word_lists=WordLists, dictionaries=Dictionaries)

    @app.context_processor
    def inject_current_year() -> dict[str, str]:  # type: ignore
        return {"CURRENT_YEAR": str(datetime.now().year)}

    init_routes(app)
    init_caches(cache_size=config_class.MAX_CACHE_SIZE)
    load_word_lists()

    _logger.info(f"create_app completed")
    return app
