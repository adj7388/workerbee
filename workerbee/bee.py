from dataclasses import asdict
from itertools import groupby

from .config import Config
from .constants import Consts
from .dictionaries import Dictionary
from .types import Beeword, Metadata, NestedBeewords, OutputData
from .wordlists import WordList


def _check_bingo(data: list[Beeword], pangram_set: set) -> bool:
    initials_set = set([beeword.word[0] for beeword in data])
    return initials_set == pangram_set


def _get_metadata(
    data: list[Beeword],
    required: str,
    allowed: str,
    dictionary: Dictionary,
    word_list: WordList,
) -> Metadata:
    return Metadata(
        num_beewords=len(data),
        required=required,
        allowed=allowed,
        bingo=_check_bingo(data, set(required + allowed)),
        perfect_pangrams=[beeword for beeword in data if beeword.is_perfect],
        nonperfect_pangrams=[
            beeword for beeword in data if beeword.is_pangram and not beeword.is_perfect
        ],
        dictionary=dictionary.name,
        word_list=word_list.name,
        beeword_fieldnames=list(asdict(data[0]).keys()) if len(data) != 0 else [],
    )


def _get_pangram_status(word: str, pangram_set: set) -> tuple:
    is_pangram = bool(set(word) == pangram_set)
    is_perfect = bool(
        is_pangram
        and len(word) == (Config.NUM_ALLOWED_LETTERS + Config.NUM_REQUIRED_LETTERS)
    )
    return (is_pangram, is_perfect)


def _get_beeword(
    word: str, required: str, allowed: str, dictionary: Dictionary
) -> Beeword:
    is_pangram, is_perfect = _get_pangram_status(
        word=word, pangram_set=set(required + allowed)
    )
    return Beeword(
        word=word,
        length=len(word),
        initials=word[0:2],
        is_pangram=is_pangram,
        is_perfect=is_perfect,
        url=dictionary.url_template.render(word=word),
    )


def _get_beewords(
    word_list: WordList,
    required_letter: str,
    allowed_letters: str,
    dictionary: Dictionary,
) -> list[Beeword]:
    all_letters_set = set(required_letter + allowed_letters)
    beewords: list[Beeword] = []
    for this_word in word_list.data:  # type: ignore
        if required_letter in this_word and len(this_word) >= Config.MIN_WORD_LENGTH:
            this_word_as_set = set(this_word)
            if this_word_as_set.issubset(all_letters_set):
                beewords.append(
                    _get_beeword(
                        word=this_word,
                        required=required_letter,
                        allowed=allowed_letters,
                        dictionary=dictionary,
                    )
                )
    return sorted(beewords, key=lambda beeword: beeword.word)


def get_groupings(grouping: str) -> list:
    if grouping == Consts.LENGTH:
        return [Consts.LENGTH, Consts.INITIALS]
    elif grouping == Consts.INITIALS:
        return [Consts.INITIALS, Consts.LENGTH]
    elif grouping == Consts.NO_GROUPING:
        return [Consts.NO_GROUPING]
    else:
        raise ValueError(f"Bad grouping: {grouping}")


def get_beewords(
    word_list: WordList,
    required_letter: str,
    allowed_letters: str,
    dictionary: Dictionary,
    grouping: str = Consts.NO_GROUPING,
) -> OutputData:
    beewords: list[Beeword] = _get_beewords(
        word_list=word_list,
        required_letter=required_letter,
        allowed_letters=allowed_letters,
        dictionary=dictionary,
    )
    # for OutputData.nested, default to initials/length grouping
    grouping_list: list[str] = (
        get_groupings(Consts.INITIALS)
        if grouping == Consts.NO_GROUPING
        else get_groupings(grouping)
    )

    def get_group0_key(beeword: Beeword) -> str | int:
        return getattr(beeword, grouping_list[0])

    def get_group1_key(beeword: Beeword) -> str | int:
        return getattr(beeword, grouping_list[1])

    nested_beewords: NestedBeewords = {}
    for group0, data0 in groupby(
        sorted(beewords, key=get_group0_key), key=get_group0_key
    ):
        nested_beewords[group0] = {}
        for group1, data1 in groupby(
            sorted(data0, key=get_group1_key), key=get_group1_key
        ):
            nested_beewords[group0][group1] = [beeword for beeword in data1]

    return OutputData(
        flat=beewords,
        nested=nested_beewords,
        metadata=_get_metadata(
            data=beewords,
            required=required_letter,
            allowed=allowed_letters,
            dictionary=dictionary,
            word_list=word_list,
        ),
    )
