import flask
from dataclasses import asdict
from datetime import datetime
from .wordlists import WordLists
from .dictionaries import Dictionaries
from .constants import Consts
from .config import Config

app = flask.Flask(__name__)
app.config.from_object(Config())


@app.context_processor
def inject_current_year():
    return {"CURRENT_YEAR": str(datetime.now().year)}


# inject consts into Jinja for templates
app.jinja_env.globals.update(**asdict(Consts()))
app.jinja_env.globals.update(WORDLISTS=WordLists, DICTIONARIES=Dictionaries)

# Import views sets up routes as a side effect
from . import views  # pyright: ignore
