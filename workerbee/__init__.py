import flask
import os
from .wordlists import WordLists
from .config import (
    ALLOWED_LETTERS,
    ALPHABETICALLY,
    ARGS,
    ASCENDING,
    BEEWORD_VIEW,
    BYWORDLENGTH,
    DESCENDING,
    Dictionaries,
    DICTIONARY,
    GETFILE_VIEW,
    GROUPING,
    INITIALS,
    LENGTH,
    NO_GROUPING,
    PROFILE_REQUEST_ARG,
    REQUIRED_LETTER,
    SHOW_WORDS,
    SUMMARY_SORT,
    SUMMARY_VIEW,
    WORD_LIST,
    WORD_SORT,
)

app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRETBEEKEY")


# Insert all config variables into jinja environment
app.jinja_env.globals.update(
    {
        "ALLOWED_LETTERS": ALLOWED_LETTERS,
        "ALPHABETICALLY": ALPHABETICALLY,
        "ARGS": ARGS,
        "ASCENDING": ASCENDING,
        "BEEWORD_VIEW": BEEWORD_VIEW,
        "BYWORDLENGTH": BYWORDLENGTH,
        "DESCENDING": DESCENDING,
        "Dictionaries": Dictionaries,
        "DICTIONARY": DICTIONARY,
        "GETFILE_VIEW": GETFILE_VIEW,
        "GROUPING": GROUPING,
        "INITIALS": INITIALS,
        "LENGTH": LENGTH,
        "NO_GROUPING": NO_GROUPING,
        "PROFILE_REQUEST_ARG": PROFILE_REQUEST_ARG,
        "REQUIRED_LETTER": REQUIRED_LETTER,
        "SHOW_WORDS": SHOW_WORDS,
        "SUMMARY_SORT": SUMMARY_SORT,
        "SUMMARY_VIEW": SUMMARY_VIEW,
        "WORD_LIST": WORD_LIST,
        "WORD_SORT": WORD_SORT,
        "WordLists": WordLists,
    }
)

# Importing here sets up routes as a side effect
from . import views  # pyright: ignore
