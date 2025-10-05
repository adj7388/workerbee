from dataclasses import dataclass


@dataclass(frozen=True)
class Consts:

    # how to mark pangrams
    PANGRAM_MARKER: str = "*"
    PERFECT_MARKER: str = "+"

    # Session consts
    ARGS: str = "args"
    ## for showing changes to Find Words and Show Summaries form/query
    DISPLAY_CHANGES: str = "display_changes"
    ## basic query params for Find Words and Show Summaries
    REQUIRED_LETTER: str = "required"
    ALLOWED_LETTERS: str = "allowed"
    DICTIONARY: str = "dictionary"
    WORD_LIST: str = "word_list"
    ## for grouping results in Find Words and Show Summaries
    GROUPING: str = "grouping"
    INITIALS: str = "initials"
    LENGTH: str = "length"
    NO_GROUPING: str = "no_grouping"
    ## how to sort Show Summaries
    SUMMARY_SORT: str = "summary_sort"
    ASCENDING: str = "ascending"
    DESCENDING: str = "descending"
    ## whether/how to show/sort words in Summaries
    SHOW_WORDS: str = "show_words"
    WORD_SORT: str = "word_sort"
    ALPHABETICALLY: str = "alphabetically"
    BYWORDLENGTH: str = "bywordlength"
    ## id for the div where results of Find Words and Show Summaries queries are inserted
    RESULTS_CONTAINER_ID: str = "results"

    ## for download form (CSV, TXT, JSON also used as file extensions)
    FILE_TYPE: str = "file_type"
    CSV: str = "csv"
    TXT: str = "txt"
    JSON: str = "json"
    WORD_URL_CSV: str = "word_url_csv"
