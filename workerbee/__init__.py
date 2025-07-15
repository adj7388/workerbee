import flask
from .views import init_routes
from .config import Config
from .constants import Consts
from .dictionaries import Dictionaries
from .wordlists import WordLists
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

    init_routes(app)

    return app


def is_eligible(word: str, rejects) -> bool:
    rejection_reason = ""
    if any(letter.isupper() for letter in word):
        rejection_reason = f"reject: has capital: {word}\n"
    elif not word.isalpha():
        rejection_reason = f"reject: non-alpha: {word}\n"
    elif len(set(word)) > (Config.NUM_ALLOWED_LETTERS + Config.NUM_REQUIRED_LETTERS):
        rejection_reason = f"reject: too many unique letters: {word}\n"
    if rejection_reason:
        rejects.write(rejection_reason)
        return False
    return True


print("START")
# read word list data into memory for speed
with open("rejected-words.txt", mode="w") as rejects:
    for wl in WordLists.values():
        with open(wl.file_name, mode="r") as f:
            rejects.write("========" + wl.file_name + "========\n")
            wl.data = [
                line.lower()
                for line in f.read().splitlines()
                if len(line) >= Config.MIN_WORD_LENGTH and is_eligible(line, rejects)
            ]
        wl.num_words = len(wl.data)
print("DONE")
