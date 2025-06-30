import os
from collections import namedtuple

Beeword = namedtuple("Beeword", "word length initials is_pangram, is_perfect, url")
Metadata = namedtuple(
    "Metadata",
    "num_beewords required allowed bingo perfect_pangrams nonperfect_pangrams dictionary word_list beeword_fieldnames",
)
OutputData = namedtuple("OutputData", "data metadata")

# Debugging
BEEPROFILE = "BEEPROFILE"
PROFILE_REQUEST_ARG = "profile"
PROFILING = True if os.environ.get(BEEPROFILE, "") == BEEPROFILE else False

# route consts
HOME_VIEW = "/"
ABOUT_VIEW = "about"
HELP_VIEW = "help"
BEEWORD_VIEW = "beewords"
GETFILE_VIEW = "getfile"
SUMMARY_FORM_VIEW = "summary_form"
SUMMARY_VIEW = "summary"

# Session consts
ARGS = "args"
## for Find Words
REQUIRED_LETTER = "required"
ALLOWED_LETTERS = "allowed"
DICTIONARY = "dictionary"
WORD_LIST = "word_list"
## for grouping
GROUPING = "grouping"
INITIALS = "initials"
LENGTH = "length"
NO_GROUPING = "no_grouping"
## for Show Summaries
SUMMARY_SORT = "summary_sort"
ASCENDING = "ascending"
DESCENDING = "descending"
SHOW_WORDS = "show_words"
WORD_SORT = "word_sort"
ALPHABETICALLY = "alphabetically"
BYWORDLENGTH = "bywordlength"

## for downloads (also used as file extensions)
FILE_TYPE = "file_type"
CSV = "csv"
TXT = "txt"
JSON = "json"
WORD_URL_CSV = "word_url_csv"

# Other constants
NUM_REQUIRED_LETTERS = 1
NUM_ALLOWED_LETTERS = 6
MIN_WORD_LENGTH = 4
PANGRAM_MARKER = "*"
PERFECT_MARKER = "+"


# directory for word list files
WORDLIST_DIR = "data"


# Manage Dictionaries
Dictionary = namedtuple("Dictionary", "name url_template")

# Dictionary keys
MW = "MW"
WIKT = "WIKT"
DICT = "DICT"
FREE = "FREE"

from jinja2 import Template, Environment

_jinja_env = Environment(autoescape=True)


def make_url_template(source: str) -> Template:
    return _jinja_env.from_string(source)


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

del _jinja_env
