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

# Other constants
NUM_REQUIRED_LETTERS = 1
NUM_ALLOWED_LETTERS = 6
MIN_WORD_LENGTH = 4
PANGRAM_MARKER = "*"
PERFECT_MARKER = "+"


# directory for word list files
WORDLIST_DIR = "data"
