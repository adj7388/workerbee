import flask
from .config import Config
from .constants import Consts
from .dictionaries import Dictionaries
from .wordlists import WordLists
from dataclasses import asdict
from datetime import datetime

app = flask.Flask(__name__)
app.config.from_object(Config())

# inject consts into Jinja for templates
app.jinja_env.globals.update(**asdict(Consts()))
app.jinja_env.globals.update(WORDLISTS=WordLists, DICTIONARIES=Dictionaries)


@app.context_processor
def inject_current_year() -> dict[str, str]:
    return {"CURRENT_YEAR": str(datetime.now().year)}


# read word list data into memory for speed
for wl in WordLists.values():
    with open(wl.file_name, mode="r") as f:
        wl.data = [
            line for line in f.read().splitlines() if len(line) > 3 and line.isalpha()
        ]

# Import views to set up routes
from . import views  # pyright: ignore
