import flask
from dataclasses import asdict
from .wordlists import WordLists
from .dictionaries import Dictionaries
from .constants import Consts
from .config import Config

app = flask.Flask(__name__)
app.config.from_object(Config())

# inject consts into Jinja for templates
app.jinja_env.globals.update(**asdict(Consts()))
app.jinja_env.globals.update(WORDLISTS=WordLists, DICTIONARIES=Dictionaries)

# Import views sets up routes as a side effect
from . import views  # pyright: ignore
