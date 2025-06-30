import copy
import csv
import json

from io import StringIO
from typing import cast, Any
from .config import Config
from .constants import Consts
from . import types


def error_check(args: dict) -> str:
    required = args[Consts.REQUIRED_LETTER]
    allowed = args[Consts.ALLOWED_LETTERS]
    required_as_set = set(required)
    allowed_as_set = set(allowed)
    if required.isalpha() is False or allowed.isalpha() is False:
        return f'"{required}" and "{allowed}" must contain only letters'
    if len(required) != Config.NUM_REQUIRED_LETTERS:
        return f'"{required}" must be {Config.NUM_REQUIRED_LETTERS} character.'
    if len(allowed) != Config.NUM_ALLOWED_LETTERS:
        return f'"{allowed}" must be {Config.NUM_ALLOWED_LETTERS} characters'
    if len(allowed_as_set) != Config.NUM_ALLOWED_LETTERS:
        return f'"{allowed}" contains a duplicate letter.'
    if required_as_set.issubset(allowed_as_set):
        return f'The required letter "{required}" cannot also be in "{allowed}"'
    return ""


def get_filename(metadata: types.Metadata, file_type: str) -> str:
    ext = Consts.CSV if file_type in [Consts.WORD_URL_CSV, Consts.CSV] else file_type
    metadata_as_list = [
        f"{metadata.required}",
        f"{metadata.allowed}",
        f"{metadata.num_beewords}",
        f"{len(metadata.nonperfect_pangrams)}",  # how many plain pangrams
        f"{len(metadata.perfect_pangrams)}",  # how many perfect pangrams
        f"{metadata.word_list}",
        f"{metadata.dictionary}",
    ]
    return "-".join(metadata_as_list) + f".{ext}"


def flatten_grouped(beewords: dict) -> dict | list[types.Beeword]:
    flattened: list[types.Beeword] = []
    try:
        for first_level in beewords.values():
            for words in first_level.values():
                flattened.extend(words)
        return sorted(flattened, key=lambda beeword: cast(types.Beeword, beeword).word)
    except AttributeError:
        return beewords


def decorate_word(beeword: types.Beeword) -> str:
    pangram_marker = (
        Consts.PERFECT_MARKER
        if beeword.is_perfect
        else Consts.PANGRAM_MARKER if beeword.is_pangram else ""
    )
    return f"{beeword.word}{pangram_marker}"


def convert_namedtuples(obj2convert: Any) -> Any:
    if isinstance(obj2convert, tuple) and hasattr(
        obj2convert, "_fields"
    ):  # it's a namedtuple
        return {
            k: convert_namedtuples(v)
            for k, v in cast(types.Beeword, obj2convert)._asdict().items()
        }
    elif isinstance(obj2convert, list):
        return [convert_namedtuples(item) for item in obj2convert]
    elif isinstance(obj2convert, dict):
        return {k: convert_namedtuples(v) for k, v in obj2convert.items()}
    else:
        return obj2convert


def write_to_buffer(output_data: types.OutputData, file_type: str) -> StringIO:
    # local copy so as not to accidentally change incoming data
    sio = StringIO()
    beewords_copy = cast(types.OutputData, copy.deepcopy(output_data))
    if file_type in [Consts.CSV, Consts.TXT, Consts.WORD_URL_CSV]:
        # Flatten grouped data for text and csv.
        # flatten_grouped() will return data as-is if not grouped
        beewords_copy = types.OutputData(
            data=flatten_grouped(beewords_copy.data), metadata=beewords_copy.metadata
        )

    if file_type in [Consts.CSV, Consts.WORD_URL_CSV]:
        if file_type == Consts.WORD_URL_CSV:
            WORD_FIELD = "word"
            URL_FIELD = "url"
            fieldnames = [WORD_FIELD, URL_FIELD]
            beewords_copy = types.OutputData(
                data=[
                    {WORD_FIELD: decorate_word(beeword), URL_FIELD: beeword.url}
                    for beeword in beewords_copy.data
                ],
                metadata=beewords_copy.metadata,
            )
        else:
            fieldnames = beewords_copy.metadata.beeword_fieldnames
            beewords_copy = types.OutputData(
                data=convert_namedtuples(beewords_copy.data),
                metadata=beewords_copy.metadata,
            )
        csvwriter = csv.DictWriter(sio, fieldnames=fieldnames)
        csvwriter.writeheader()
        csvwriter.writerows(beewords_copy.data)

    elif file_type == Consts.TXT:
        sio.write("\n".join([decorate_word(word) for word in beewords_copy.data]))

    elif file_type == Consts.JSON:
        beewords_copy = convert_namedtuples(beewords_copy)
        sio.write(json.dumps(beewords_copy, indent=2))

    else:
        raise ValueError(f"Bad file_type: {file_type}")

    return sio
