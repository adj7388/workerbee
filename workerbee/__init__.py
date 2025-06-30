import flask
import os
from .wordlists import WordLists
from .config import (
    ABOUT_VIEW,
    ALLOWED_LETTERS,
    ALPHABETICALLY,
    ASCENDING,
    BEEWORD_VIEW,
    BYWORDLENGTH,
    DESCENDING,
    DICTIONARY,
    GETFILE_VIEW,
    GROUPING,
    INITIALS,
    # "layout.html",
    LENGTH,
    # "macros.html",
    NO_GROUPING,
    PROFILE_REQUEST_ARG,
    REQUIRED_LETTER,
    SHOW_WORDS,
    SUMMARY_SORT,
    SUMMARY_VIEW,
    WORD_LIST,
    ARGS,
    WORD_SORT,
    Dictionaries,
)

app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRETBEEKEY")


# Insert all config variables into jinja environment
app.jinja_env.globals.update(
    {
        "ABOUT_VIEW": ABOUT_VIEW,
        "ARGS": ARGS,
        "Dictionaries": Dictionaries,
        # ""layout.html"": "layout.html",
        # ""macros.html"": "macros.html",
        "WORD_LIST": WORD_LIST,
        "WordLists": WordLists,
        "BEEWORD_VIEW": BEEWORD_VIEW,
        "PROFILE_REQUEST_ARG": PROFILE_REQUEST_ARG,
        "REQUIRED_LETTER": REQUIRED_LETTER,
        "ALLOWED_LETTERS": ALLOWED_LETTERS,
        "GROUPING": GROUPING,
        "INITIALS": INITIALS,
        "LENGTH": LENGTH,
        "NO_GROUPING": NO_GROUPING,
        "GETFILE_VIEW": GETFILE_VIEW,
        "SUMMARY_VIEW": SUMMARY_VIEW,
        "SUMMARY_SORT": SUMMARY_SORT,
        "ASCENDING": ASCENDING,
        "DESCENDING": DESCENDING,
        "SHOW_WORDS": SHOW_WORDS,
        "BYWORDLENGTH": BYWORDLENGTH,
        "ALPHABETICALLY": ALPHABETICALLY,
        "DICTIONARY": DICTIONARY,
        "WORD_SORT": WORD_SORT,
    }
)

# Importing here sets up routes as a side effect
from . import views  # pyright: ignore
