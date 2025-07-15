import flask
from .views import init_routes
from .config import Config
from .constants import Consts
from .dictionaries import Dictionaries
from .wordlists import WordLists, load_word_lists
from dataclasses import asdict
from datetime import datetime


def create_app(config_class=Config) -> flask.Flask:
    app = flask.Flask(__name__)
    app.config.from_object(config_class())

    # inject consts into Jinja for templates
    app.jinja_env.globals.update(**asdict(Consts()))
    app.jinja_env.globals.update(WORDLISTS=WordLists, DICTIONARIES=Dictionaries)

    @app.context_processor
    def inject_current_year() -> dict[str, str]:  # type: ignore
        return {"CURRENT_YEAR": str(datetime.now().year)}

    load_word_lists()

    init_routes(app)

    return app
