from dataclasses import dataclass
from typing import TypeAlias


@dataclass(slots=True)
class SpellingBeeWord:
    word: str
    length: int
    initials: str
    is_pangram: bool
    is_perfect: bool
    definition_url: str


@dataclass(slots=True)
class PangramStatus:
    is_pangram: bool
    is_perfect: bool


@dataclass(slots=True)
class Metadata:
    num_beewords: int
    required: str
    allowed: str
    bingo: bool
    perfect_pangrams: list[SpellingBeeWord]
    nonperfect_pangrams: list[SpellingBeeWord]
    dictionary: str
    word_list: str
    beeword_fieldnames: list[str]


NestedKeyType: TypeAlias = str | int
NestedSpellingBeeWords: TypeAlias = dict[
    NestedKeyType, dict[NestedKeyType, list[SpellingBeeWord]]
]


@dataclass(slots=True)
class FindWordsOutput:
    nested: NestedSpellingBeeWords
    flat: list[SpellingBeeWord]
    metadata: Metadata


@dataclass(slots=True)
class ShowSummariesOutput:
    beewords: dict[NestedKeyType, list[SpellingBeeWord]]
    metadata: Metadata
