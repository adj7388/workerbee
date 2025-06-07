import copy
import csv
import json

from io import StringIO

from . import config


def error_check(args: dict) -> str:
    required = args[config.REQUIRED_LETTER]
    allowed = args[config.ALLOWED_LETTERS]
    required_as_set = set(required)
    allowed_as_set = set(allowed)
    if required.isalpha() is False or allowed.isalpha() is False:
        return f'"{required}" and "{allowed}" must contain only letters'
    if len(required) != config.NUM_REQUIRED_LETTERS:
        return f'"{required}" must be {config.NUM_REQUIRED_LETTERS} character.'
    if len(allowed) != config.NUM_ALLOWED_LETTERS:
        return f'"{allowed}" must be {config.NUM_ALLOWED_LETTERS} characters'
    if len(allowed_as_set) != config.NUM_ALLOWED_LETTERS:
        return f'"{allowed}" contains a duplicate letter.'
    if required_as_set.issubset(allowed_as_set):
        return f'The required letter "{required}" cannot also be in "{allowed}"'
    return ""


def clean_args(args: dict) -> dict:
    return {
        config.REQUIRED_LETTER: args[config.REQUIRED_LETTER].lower().strip(),
        config.ALLOWED_LETTERS: args[config.ALLOWED_LETTERS].lower().strip(),
        config.GROUPING: args[config.GROUPING],
        config.DICTIONARY: args[config.DICTIONARY],
        config.WORD_LIST: args[config.WORD_LIST],
    }


def get_filename(metadata: dict, file_type: str) -> str:
    ext = config.CSV if file_type in [config.WORD_URL_CSV, config.CSV] else file_type
    return (
        f"{metadata[config.REQUIRED_LETTER]}-"
        f"{metadata[config.ALLOWED_LETTERS]}-"
        f"{metadata[config.NUM_BEEWORDS]}-"
        f"{len(metadata[config.NONPERFECT_PANGRAMS])}-"  # how many plain pangrams
        f"{len(metadata[config.PERFECT_PANGRAMS])}-"  # how many perfect pangrams
        f"{metadata[config.DICTIONARY]}"
        f".{ext}"
    )


def flatten_grouped(beewords) -> list[dict]:
    flattened = []
    try:
        for first_level in beewords.values():
            for words in first_level.values():
                flattened.extend(words)
        return sorted(flattened, key=lambda word: word[config.WORD])
    except AttributeError:
        return beewords


def decorate_word(word: dict) -> str:
    pangram_marker = (
        config.PERFECT_MARKER
        if word[config.IS_PERFECT]
        else config.PANGRAM_MARKER if word[config.IS_PANGRAM] else ""
    )
    return f"{word[config.WORD]}{pangram_marker}"


def write_to_buffer(beewords: dict, file_type: str) -> StringIO:
    # local copy so as not to accidentally change incoming data
    beewords_copy = copy.deepcopy(beewords)
    if file_type in [config.CSV, config.TXT, config.WORD_URL_CSV]:
        # Flatten grouped data for text and csv.
        # flatten_grouped() will return data as-is if not grouped
        beewords_copy[config.DATA] = flatten_grouped(beewords_copy[config.DATA])

    sio = StringIO()

    if file_type in [config.CSV, config.WORD_URL_CSV]:
        if file_type == config.WORD_URL_CSV:
            fieldnames = [config.WORD, config.URL]
            beewords_copy[config.DATA] = [
                {config.WORD: decorate_word(word), config.URL: word[config.URL]}
                for word in beewords_copy[config.DATA]
            ]
        else:
            fieldnames = beewords_copy[config.METADATA][config.BEEWORD_FIELDNAMES]
        csvwriter = csv.DictWriter(sio, fieldnames=fieldnames)
        csvwriter.writeheader()
        csvwriter.writerows(beewords_copy[config.DATA])

    elif file_type == config.TXT:
        sio.write(
            "\n".join([decorate_word(word) for word in beewords_copy[config.DATA]])
        )

    elif file_type == config.JSON:
        sio.write(json.dumps(beewords_copy, indent=2))

    else:
        raise ValueError(f"Bad file_type: {file_type}")

    return sio
