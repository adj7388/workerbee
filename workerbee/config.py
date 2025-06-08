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
HELP_TEMPLATE = "help.html"
BEEWORDS_TEMPLATE = "beewords.html"
LISTWORDS_TEMPLATE = "listwords.html"
ERROR_TEMPLATE = "error.html"

# route consts
HOME_VIEW = "/"
ABOUT_VIEW = "about"
HELP_VIEW = "help"
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
WORD_LIST = "word_list"

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


# Manage Word Lists
WordList = namedtuple("WordList", "name file_name")

# Word list keys
DWYL = "DWYL"
LINUX_US = "LINUX-US"
LINUX_UK = "LINUX-UK"
SCOWL_10 = "SCOWL-10"
SCOWL_20 = "SCOWL-20"
SCOWL_SMALL_35 = "SCOWL-SMALL-35"
SCOWL_40 = "SCOWL-40"
SCOWL_MEDIUM_50 = "SCOWL-MEDIUM-50"
SCOWL_55 = "SCOWL-55"
SCOWL_DEFAULT_60 = "SCOWL-DEFAULT-60"
SCOWL_LARGE_70 = "SCOWL-LARGE-70"
SCOWL_HUGE_80 = "SCOWL-HUGE-80"
SCOWL_INSANE_95 = "SCOWL-INSANE-95"

WordLists = {
    DWYL: WordList(name="DWYL Words (dwyl.com)", file_name=f"{DWYL}/alpha_words.txt"),
    LINUX_UK: WordList(
        name="Linux British English", file_name=f"{LINUX_UK}/british-english"
    ),
    LINUX_US: WordList(
        name="Linux American English", file_name=f"{LINUX_US}/american-english"
    ),
    SCOWL_10: WordList(
        name=f"{SCOWL_10}", file_name=f"{SCOWL_10}/words.txt"
    ),
    SCOWL_20: WordList(
        name=f"{SCOWL_20}", file_name=f"{SCOWL_20}/words.txt"
    ),
    SCOWL_SMALL_35: WordList(
        name=f"{SCOWL_SMALL_35}", file_name=f"{SCOWL_SMALL_35}/words.txt"
    ),
    SCOWL_40: WordList(
        name=f"{SCOWL_40}", file_name=f"{SCOWL_40}/words.txt"
    ),
    SCOWL_MEDIUM_50: WordList(
        name=f"{SCOWL_MEDIUM_50}", file_name=f"{SCOWL_MEDIUM_50}/words.txt"
    ),
    SCOWL_55: WordList(
        name=f"{SCOWL_55}", file_name=f"{SCOWL_55}/words.txt"
    ),
    SCOWL_DEFAULT_60: WordList(
        name=f"{SCOWL_DEFAULT_60}", file_name=f"{SCOWL_DEFAULT_60}/words.txt"
    ),
    SCOWL_LARGE_70: WordList(
        name=f"{SCOWL_LARGE_70}", file_name=f"{SCOWL_LARGE_70}/words.txt"
    ),
    SCOWL_HUGE_80: WordList(
        name=f"{SCOWL_HUGE_80}", file_name=f"{SCOWL_HUGE_80}/words.txt"
    ),
    SCOWL_INSANE_95: WordList(
        name=f"{SCOWL_INSANE_95}", file_name=f"{SCOWL_INSANE_95}/words.txt"
    ),
}

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
