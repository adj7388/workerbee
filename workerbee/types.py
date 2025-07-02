from collections import namedtuple
from dataclasses import dataclass

from workerbee.dictionaries import Dictionary
from workerbee.wordlists import WordList

Beeword = namedtuple("Beeword", "word length initials is_pangram, is_perfect, url")


@dataclass
class Metadata:
    num_beewords: int
    required: str
    allowed: str
    bingo: bool
    perfect_pangrams: list[Beeword]
    nonperfect_pangrams: list[Beeword]
    dictionary: Dictionary
    word_list: WordList
    beeword_fieldnames: list[str]


@dataclass
class OutputData:
    nested: dict[str, dict[str, list[Beeword]]]
    flat: list[Beeword]
    metadata: Metadata


@dataclass
class Summary:
    beewords: dict[str, list[Beeword]]
    metadata: Metadata
