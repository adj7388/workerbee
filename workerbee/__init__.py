import flask
import os

from dataclasses import asdict
from datetime import datetime

from .config import Config, DevConfig, ProdConfig
from .constants import Consts
from .dictionaries import Dictionaries
from .views import init_routes
from .wordlists import WordLists, load_word_lists
from .logging_setup import configure_logging


def create_app(config_class=DevConfig) -> flask.Flask | None:
    config_name = os.getenv("FLASK_CONFIG", "Config")
    config_class = {
        "Config": Config,
        "DevConfig": DevConfig,
        "ProdConfig": ProdConfig,
    }.get(config_name, "Config")

    configure_logging(level=config_class.LOG_LEVEL)

    app = flask.Flask(__name__)
    app.config.from_object(config_class)

    load_word_lists()
    init_routes(app)

    # inject consts into Jinja for templates
    app.jinja_env.globals.update(**asdict(Consts()))
    app.jinja_env.globals.update(word_lists=WordLists, dictionaries=Dictionaries)

    @app.context_processor
    def inject_current_year() -> dict[str, str]:  # type: ignore
        return {"CURRENT_YEAR": str(datetime.now().year)}

    return app
