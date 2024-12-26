import os
from collections import namedtuple
from jinja2 import Environment, Template, FileSystemLoader

# Debugging
BEEPROFILE = "BEEPROFILE"
PROFILE_REQUEST_ARG = "profile"
PROFILING = True if os.environ.get(BEEPROFILE, "") == BEEPROFILE else False

# template and file consts
APP_FOLDER = "workerbee"
TEMPLATE_FOLDER = f"{APP_FOLDER}/templates"
TEMP_FOLDER = "temp"
STATIC_FOLDER = "static"
SITE_CSS = "site.css"

LAYOUT_TEMPLATE = "layout.html"
MACROS_TEMPLATE = "macros.html"
HOME_TEMPLATE = "home.html"
ABOUT_TEMPLATE = "about.html"
BEEWORDS_TEMPLATE = "beewords.html"
LISTWORDS_TEMPLATE = "listwords.html"
ERROR_TEMPLATE = "error.html"

# route consts
HOME_VIEW = "/"
ABOUT_VIEW = "about"
BEEWORD_VIEW = "beewords"
GETFILE_VIEW = "getfile"

# Metadata consts
METADATA = "metadata"
NUM_BEEWORDS = "num_beewords"
REQUIRED_LETTER = "required"
ALLOWED_LETTERS = "allowed"
BINGO = "bingo"
NONPERFECT_PANGRAMS = "nonperfect_pangrams"
PERFECT_PANGRAMS = "perfect_pangrams"
DICTIONARY = "dictionary"
BEEWORD_FIELDNAMES = "beeword_fieldnames"

# Data and beeword consts
DATA = "data"
WORD = "word"
IS_PANGRAM = "pangram"
IS_PERFECT = "perfect"
URL = "url"

# grouping consts
GROUPING = "grouping"
INITIALS = "initials"
LENGTH = "length"
NO_GROUPING = "no_grouping"

# file download types
CSV = "csv"
TXT = "txt"
JSON = "json"
WORD_URL_CSV = "word_url_csv"

# session keys
USER_ARGS = "user_args"
FILE_TYPE = "file_type"

# Other constants
NUM_REQUIRED_LETTERS = 1
NUM_ALLOWED_LETTERS = 6
MIN_WORD_LENGTH = 4
PANGRAM_MARKER = "*"
PERFECT_MARKER = "+"

JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))


def make_url_template(source: str) -> Template:
    return JINJA_ENV.from_string(source)


# Manage Dictionaries
Dictionary = namedtuple("Dictionary", "name url_template")

# Dictionary keys
MW = "MW"
WIKT = "WIKT"
DICT = "DICT"
FREE = "FREE"

Dictionaries = {
    MW: Dictionary(
        name="Merriam-Webster",
        url_template=make_url_template(
            "https://www.merriam-webster.com/dictionary/{{ word }}"
        ),
    ),
    WIKT: Dictionary(
        name="Wiktionary",
        url_template=make_url_template(
            "https://en.wiktionary.org/wiki/{{ word }}#English"
        ),
    ),
    DICT: Dictionary(
        name="Dictionary.com",
        url_template=make_url_template("https://www.dictionary.com/browse/{{ word }}"),
    ),
    FREE: Dictionary(
        name="Free Dictionary",
        url_template=make_url_template("https://www.thefreedictionary.com/{{ word }}"),
    ),
}

# import flask functions so they are inserted into Jinja globals
from flask import url_for, get_flashed_messages, session

# Assign const variables to jinja environment after all are defined
JINJA_ENV.globals.update(locals())
