from itertools import groupby

from workerbee import wordlists

from .config import Config
from .constants import Consts
from . import dictionaries as dicts
from . import wordlists
from . import types


def get_groupings(grouping: str) -> list:
    if grouping == Consts.LENGTH:
        return [Consts.LENGTH, Consts.INITIALS]
    elif grouping == Consts.INITIALS:
        return [Consts.INITIALS, Consts.LENGTH]
    elif grouping == Consts.NO_GROUPING:
        return [Consts.NO_GROUPING]
    else:
        raise ValueError(f"Bad grouping: {grouping}")


def check_bingo(data: list[types.Beeword], pangram_set: set) -> bool:
    initials_set = set([beeword.word[0] for beeword in data])
    return initials_set == pangram_set


def get_metadata(
    data: list[types.Beeword],
    required: str,
    allowed: str,
    dictionary: dicts.Dictionary,
    word_list: wordlists.WordList,
) -> types.Metadata:
    return types.Metadata(
        num_beewords=len(data),
        required=required,
        allowed=allowed,
        bingo=check_bingo(data, set(required + allowed)),
        perfect_pangrams=[beeword for beeword in data if beeword.is_perfect],
        nonperfect_pangrams=[
            beeword for beeword in data if beeword.is_pangram and not beeword.is_perfect
        ],
        dictionary=dictionary.name,
        word_list=word_list.name,
        beeword_fieldnames=list(data[0]._fields) if data else "",
    )


def get_pangram_status(word: str, pangram_set: set) -> tuple:
    is_pangram = bool(set(word) == pangram_set)
    is_perfect = bool(
        is_pangram
        and len(word) == (Config.NUM_ALLOWED_LETTERS + Config.NUM_REQUIRED_LETTERS)
    )
    return (is_pangram, is_perfect)


def _get_beeword(
    word: str, required: str, allowed: str, dictionary: dicts.Dictionary
) -> types.Beeword:
    is_pangram, is_perfect = get_pangram_status(
        word=word, pangram_set=set(required + allowed)
    )
    return types.Beeword(
        word=word,
        length=len(word),
        initials=word[0:2],
        is_pangram=is_pangram,
        is_perfect=is_perfect,
        url=dictionary.url_template.render(word=word),
    )


def _get_beewords(
    word_list: wordlists.WordList,
    required_letter: str,
    allowed_letters: str,
    dictionary: dicts.Dictionary,
) -> types.OutputData:
    with open(word_list.file_name, mode="r") as f:
        words = [line for line in f.read().splitlines()]
    all_letters_set = set(required_letter + allowed_letters)
    beewords: list[types.Beeword] = []
    for this_word in words:
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
    beewords = sorted(beewords, key=lambda beeword: beeword.word)
    return types.OutputData(
        nested={},
        flat=beewords,
        metadata=get_metadata(
            data=beewords,
            required=required_letter,
            allowed=allowed_letters,
            dictionary=dictionary,
            word_list=word_list,
        ),
    )


def get_beewords(
    word_list: wordlists.WordList,
    required_letter: str,
    allowed_letters: str,
    dictionary: dicts.Dictionary,
    grouping: list[str],  # = ,
) -> types.OutputData:
    beewords = _get_beewords(
        word_list=word_list,
        required_letter=required_letter,
        allowed_letters=allowed_letters,
        dictionary=dictionary,
    )
    grouping = (
        # default to initials/length
        [Consts.INITIALS, Consts.LENGTH]
        if grouping == [Consts.NO_GROUPING]
        else grouping
    )

    def get_group0_key(beeword: types.Beeword):
        return getattr(beeword, grouping[0])

    def get_group1_key(beeword: types.Beeword):
        return getattr(beeword, grouping[1])

    beewords_list = beewords.flat
    nested_beewords = {}
    for group0, data0 in groupby(
        sorted(beewords_list, key=get_group0_key), key=get_group0_key
    ):
        nested_beewords[group0] = {}
        for group1, data1 in groupby(
            sorted(data0, key=get_group1_key), key=get_group1_key
        ):
            nested_beewords[group0][group1] = [beeword for beeword in data1]

    return types.OutputData(
        flat=beewords_list, nested=nested_beewords, metadata=beewords.metadata
    )
