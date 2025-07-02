from dataclasses import dataclass

from workerbee.dictionaries import Dictionary
from workerbee.wordlists import WordList


@dataclass
class Beeword:
    word: str
    length: int
    initials: str
    is_pangram: bool
    is_perfect: bool
    url: str


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
