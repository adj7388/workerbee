from dataclasses import dataclass
from typing import TypeAlias


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
    dictionary: str
    word_list: str
    beeword_fieldnames: list[str]


NestedKeyType: TypeAlias = str | int
NestedBeewords: TypeAlias = dict[NestedKeyType, dict[NestedKeyType, list[Beeword]]]


@dataclass
class OutputData:
    nested: NestedBeewords
    flat: list[Beeword]
    metadata: Metadata


@dataclass
class Summary:
    beewords: dict[str, list[Beeword]]
    metadata: Metadata
