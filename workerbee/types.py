from collections import namedtuple
from dataclasses import dataclass

Beeword = namedtuple("Beeword", "word length initials is_pangram, is_perfect, url")
Metadata = namedtuple(
    "Metadata",
    "num_beewords required allowed bingo perfect_pangrams nonperfect_pangrams dictionary word_list beeword_fieldnames",
)


@dataclass
class OutputData:
    nested: dict[str, dict[str, list[Beeword]]]
    flat: list[Beeword]
    metadata: Metadata


@dataclass
class Summary:
    beewords: dict[str, list[Beeword]]
    metadata: Metadata
