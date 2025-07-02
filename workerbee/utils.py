from dataclasses import asdict, is_dataclass
from io import StringIO
from typing import Any
import csv
import json

from .config import Config
from .constants import Consts
from .types import Beeword, Metadata, OutputData


def error_check(args: dict) -> str:
    required = args[Consts.REQUIRED_LETTER]
    allowed = args[Consts.ALLOWED_LETTERS]
    required_as_set = set(required)
    allowed_as_set = set(allowed)
    if required == "" or allowed == "":
        return f'Neither "required" nor "other" letters can be blank'
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


def get_filename(metadata: Metadata, file_type: str) -> str:
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


def decorate_word(beeword: Beeword) -> str:
    pangram_marker = (
        Consts.PERFECT_MARKER
        if beeword.is_perfect
        else Consts.PANGRAM_MARKER if beeword.is_pangram else ""
    )
    return f"{beeword.word}{pangram_marker}"


def make_serializable(obj2convert: Any) -> Any:
    if isinstance(obj2convert, tuple) and hasattr(
        obj2convert, "_fields"
    ):  # it's a namedtuple
        return {
            k: make_serializable(v)
            for k, v in obj2convert._asdict().items()  # type: ignore[attr-defined]
        }
    elif isinstance(obj2convert, list):
        return [make_serializable(item) for item in obj2convert]
    elif isinstance(obj2convert, dict):
        return {k: make_serializable(v) for k, v in obj2convert.items()}
    elif is_dataclass(obj2convert) and not isinstance(obj2convert, type):
        # it's a dataclass instance, not a dataclass class
        return {k: make_serializable(v) for k, v in asdict(obj2convert).items()}
    else:
        return obj2convert


def write_to_buffer(
    output_data: OutputData, file_type: str, grouping: str = Consts.NO_GROUPING
) -> StringIO:
    csv_output: list[dict] = []
    sio = StringIO()
    if file_type in [Consts.CSV, Consts.WORD_URL_CSV]:
        if file_type == Consts.WORD_URL_CSV:
            WORD_FIELD = "word"
            URL_FIELD = "url"
            fieldnames = [WORD_FIELD, URL_FIELD]
            csv_output = [
                {WORD_FIELD: decorate_word(beeword), URL_FIELD: beeword.url}
                for beeword in output_data.flat
            ]
        if file_type == Consts.CSV:
            fieldnames = output_data.metadata.beeword_fieldnames
            csv_output = make_serializable(output_data.flat)
        csvwriter = csv.DictWriter(sio, fieldnames=fieldnames)
        csvwriter.writeheader()
        csvwriter.writerows(csv_output)

    elif file_type == Consts.TXT:
        sio.write("\n".join([decorate_word(word) for word in output_data.flat]))

    elif file_type == Consts.JSON:
        data = (
            output_data.flat if grouping == Consts.NO_GROUPING else output_data.nested
        )
        sio.write(
            json.dumps(
                make_serializable({"data": data, "metadata": output_data.metadata}),
                indent=2,
            )
        )

    else:
        raise ValueError(f"Bad file_type: {file_type}")

    return sio
