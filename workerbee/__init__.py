import flask
import os
from dataclasses import asdict
from .wordlists import WordLists
from .dictionaries import Dictionaries
from .constants import Consts

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRETBEEKEY")
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "false").lower() == "true"
app.config[Consts.PROFILING] = (
    True
    if os.environ.get(Consts.BEEPROFILE, "").lower() == Consts.BEEPROFILE.lower()
    else False
)

# inject consts into Jinja for templates
app.jinja_env.globals.update(**asdict(Consts()))
app.jinja_env.globals.update(WordLists=WordLists, Dictionaries=Dictionaries)

# Import views sets up routes as a side effect
from . import views  # pyright: ignore
