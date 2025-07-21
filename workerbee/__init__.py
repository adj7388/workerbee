import flask
import logging

from dataclasses import asdict
from datetime import datetime

from .config import Config
from .constants import Consts
from .dictionaries import Dictionaries
from .views import init_routes
from .wordlists import WordLists, load_word_lists
from .logging_setup import configure_logging


def create_app(config_class=Config, cli_mode=False) -> flask.Flask | None:

    configure_logging(level=logging.INFO)

    app = flask.Flask(__name__)
    app.config.from_object(config_class())
    app.logger.info(f"Running web app")
    load_word_lists()
    init_routes(app)

    # inject consts into Jinja for templates
    app.jinja_env.globals.update(**asdict(Consts()))
    app.jinja_env.globals.update(word_lists=WordLists, dictionaries=Dictionaries)

    @app.context_processor
    def inject_current_year() -> dict[str, str]:  # type: ignore
        return {"CURRENT_YEAR": str(datetime.now().year)}

    return app
