import flask
import logging
from logging.handlers import RotatingFileHandler

from dataclasses import asdict
from datetime import datetime

from .config import Config
from .constants import Consts
from .dictionaries import Dictionaries
from .views import init_routes
from .wordlists import WordLists, load_word_lists


def create_app(config_class=Config, cli_mode=False) -> flask.Flask:
    app = flask.Flask(__name__)
    app.config.from_object(config_class())

    handler = RotatingFileHandler("workerbee.log", maxBytes=100000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info(f"Logging enabled")

    if not cli_mode:
        load_word_lists(app)
        init_routes(app)

        # inject consts into Jinja for templates
        app.jinja_env.globals.update(**asdict(Consts()))
        app.jinja_env.globals.update(word_lists=WordLists, dictionaries=Dictionaries)

        @app.context_processor
        def inject_current_year() -> dict[str, str]:  # type: ignore
            return {"CURRENT_YEAR": str(datetime.now().year)}

    return app
