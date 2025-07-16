import time

from dataclasses import dataclass
from typing import TextIO

from .config import Config


@dataclass(slots=True)
class WordList:
    name: str
    file_name: str
    data: list[str] | None = None
    num_words: int | None = None


WORDLIST_DIR = "data"
# Word list keys
SCOWL_SMALL_35 = "SCOWL-small-35"
SCOWL_40 = "SCOWL-40"
SCOWL_MEDIUM_50 = "SCOWL-medium-50"
SCOWL_55 = "SCOWL-55"
SCOWL_DEFAULT_60 = "SCOWL-default-60"
SCOWL_LARGE_70 = "SCOWL-large-70"
SCOWL_HUGE_80 = "SCOWL-huge-80"
SCOWL_INSANE_95 = "SCOWL-insane-95"
TWELVEDICTS_2of12 = "12dicts-2of12"
TWELVEDICTS_2of12inf = "12dicts-2of12inf"
TWELVEDICTS_3esl = "12dicts-3esl"
TWELVEDICTS_6of12 = "12dicts-6of12"
TWELVEDICTS_602_DIR = "12dicts-6.0.2"

WordLists = {
    SCOWL_SMALL_35: WordList(
        name=f"{SCOWL_SMALL_35}",
        file_name=f"{WORDLIST_DIR}/{SCOWL_SMALL_35}/words.txt",
    ),
    SCOWL_40: WordList(
        name=f"{SCOWL_40}",
        file_name=f"{WORDLIST_DIR}/{SCOWL_40}/words.txt",
    ),
    SCOWL_MEDIUM_50: WordList(
        name=f"{SCOWL_MEDIUM_50}",
        file_name=f"{WORDLIST_DIR}/{SCOWL_MEDIUM_50}/words.txt",
    ),
    SCOWL_55: WordList(
        name=f"{SCOWL_55}",
        file_name=f"{WORDLIST_DIR}/{SCOWL_55}/words.txt",
    ),
    SCOWL_DEFAULT_60: WordList(
        name=f"{SCOWL_DEFAULT_60}",
        file_name=f"{WORDLIST_DIR}/{SCOWL_DEFAULT_60}/words.txt",
    ),
    SCOWL_LARGE_70: WordList(
        name=f"{SCOWL_LARGE_70}",
        file_name=f"{WORDLIST_DIR}/{SCOWL_LARGE_70}/words.txt",
    ),
    SCOWL_HUGE_80: WordList(
        name=f"{SCOWL_HUGE_80}",
        file_name=f"{WORDLIST_DIR}/{SCOWL_HUGE_80}/words.txt",
    ),
    SCOWL_INSANE_95: WordList(
        name=f"{SCOWL_INSANE_95}",
        file_name=f"{WORDLIST_DIR}/{SCOWL_INSANE_95}/words.txt",
    ),
    TWELVEDICTS_2of12: WordList(
        name="12dicts-2of12",
        file_name=f"{WORDLIST_DIR}/{TWELVEDICTS_602_DIR}/2of12.txt",
    ),
    TWELVEDICTS_2of12inf: WordList(
        name="12dicts-2of12inf",
        file_name=f"{WORDLIST_DIR}/{TWELVEDICTS_602_DIR}/2of12inf.txt",
    ),
    TWELVEDICTS_3esl: WordList(
        name="12dicts-3esl",
        file_name=f"{WORDLIST_DIR}/{TWELVEDICTS_602_DIR}/3esl.txt",
    ),
    TWELVEDICTS_6of12: WordList(
        name="12dicts-6of12",
        file_name=f"{WORDLIST_DIR}/{TWELVEDICTS_602_DIR}/6of12.txt",
    ),
}


def is_beeword_candidate(word: str, rejects: TextIO) -> bool:
    rejection_reason = ""
    if any(letter.isupper() for letter in word):
        rejection_reason = f"has capital letter: {word}\n"
    elif not word.isalpha():
        rejection_reason = f"not all alphanumeric: {word}\n"
    elif len(word.strip()) < Config.MIN_WORD_LENGTH:
        rejection_reason = f"too short: {word}\n"
    elif len(set(word)) > (Config.NUM_ALLOWED_LETTERS + Config.NUM_REQUIRED_LETTERS):
        rejection_reason = f"too many unique letters: {word}\n"
    if rejection_reason:
        rejects.write(rejection_reason)
        return False
    return True


def load_word_lists(*list_keys: str) -> str:
    # read word list data into memory for speed
    load_list = (
        [WordLists[key] for key in list_keys] if list_keys else WordLists.values()
    )

    start = time.perf_counter()
    if load_list:
        rejects: TextIO
        with open("rejected-words.txt", mode="w") as rejects:
            for wl in load_list:
                with open(wl.file_name, mode="r") as f:
                    rejects.write(f"{'=' * 8} + {wl.file_name} + {'=' * 8}\n")
                    wl.data = [
                        line
                        for line in f.read().splitlines()
                        if is_beeword_candidate(line, rejects)
                    ]
                wl.num_words = len(wl.data)
    end = time.perf_counter()
    msg = f"Loaded: {"  ".join(sorted([wl.name for wl in load_list])) if load_list else 'None'}\nLoad time: {end - start:.6f} seconds"
    print(msg)
    return msg
