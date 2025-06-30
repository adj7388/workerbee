from collections import namedtuple

Beeword = namedtuple("Beeword", "word length initials is_pangram, is_perfect, url")
Metadata = namedtuple(
    "Metadata",
    "num_beewords required allowed bingo perfect_pangrams nonperfect_pangrams dictionary word_list beeword_fieldnames",
)
OutputData = namedtuple("OutputData", "data metadata")
