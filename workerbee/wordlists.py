from dataclasses import dataclass


@dataclass
class WordList:
    name: str
    file_name: str


WORDLIST_DIR = "data"
# Word list keys
SCOWL_SMALL_35 = "SCOWL-SMALL-35"
SCOWL_40 = "SCOWL-40"
SCOWL_MEDIUM_50 = "SCOWL-MEDIUM-50"
SCOWL_55 = "SCOWL-55"
SCOWL_DEFAULT_60 = "SCOWL-DEFAULT-60"
SCOWL_LARGE_70 = "SCOWL-LARGE-70"
SCOWL_HUGE_80 = "SCOWL-HUGE-80"
SCOWL_INSANE_95 = "SCOWL-INSANE-95"
TWELVEDICTS_2of12 = "12dicts-2of12"
TWELVEDICTS_2of12inf = "12dicts-2of12inf"
TWELVEDICTS_3esl = "12dicts-3esl"
TWELVEDICTS_6of12 = "12dicts-6of12"
TWELVEDICTS_602_DIR = "12dicts-6.0.2"

WordLists = {
    SCOWL_DEFAULT_60: WordList(
        name=f"{SCOWL_DEFAULT_60}",
        file_name=f"{WORDLIST_DIR}/{SCOWL_DEFAULT_60}/words.txt",
    ),
    SCOWL_SMALL_35: WordList(
        name=f"{SCOWL_SMALL_35}", file_name=f"{WORDLIST_DIR}/{SCOWL_SMALL_35}/words.txt"
    ),
    SCOWL_40: WordList(
        name=f"{SCOWL_40}", file_name=f"{WORDLIST_DIR}/{SCOWL_40}/words.txt"
    ),
    SCOWL_MEDIUM_50: WordList(
        name=f"{SCOWL_MEDIUM_50}",
        file_name=f"{WORDLIST_DIR}/{SCOWL_MEDIUM_50}/words.txt",
    ),
    SCOWL_55: WordList(
        name=f"{SCOWL_55}", file_name=f"{WORDLIST_DIR}/{SCOWL_55}/words.txt"
    ),
    SCOWL_LARGE_70: WordList(
        name=f"{SCOWL_LARGE_70}", file_name=f"{WORDLIST_DIR}/{SCOWL_LARGE_70}/words.txt"
    ),
    SCOWL_HUGE_80: WordList(
        name=f"{SCOWL_HUGE_80}", file_name=f"{WORDLIST_DIR}/{SCOWL_HUGE_80}/words.txt"
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
        name="12dicts-3esl", file_name=f"{WORDLIST_DIR}/{TWELVEDICTS_602_DIR}/3esl.txt"
    ),
    TWELVEDICTS_6of12: WordList(
        name="12dicts-6of12",
        file_name=f"{WORDLIST_DIR}/{TWELVEDICTS_602_DIR}/6of12.txt",
    ),
}
