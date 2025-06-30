from dataclasses import dataclass
from jinja2 import Template, Environment

_jinja_env = Environment(autoescape=True)


def make_url_template(source: str) -> Template:
    return _jinja_env.from_string(source)


@dataclass
class Dictionary:
    name: str
    url_template: Template


# Dictionaries keys
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
