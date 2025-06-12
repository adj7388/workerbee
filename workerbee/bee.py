from collections import namedtuple
from itertools import groupby

import re
from . import config


def get_groupings(grouping: str) -> list:
    if grouping == config.LENGTH:
        return [config.LENGTH, config.INITIALS]
    elif grouping == config.INITIALS:
        return [config.INITIALS, config.LENGTH]
    elif grouping == config.NO_GROUPING:
        return [config.NO_GROUPING]
    else:
        raise ValueError(f"Bad grouping: {grouping}")


def check_bingo(data: list[config.Beeword], pangram_set: set) -> bool:
    initials_set = set([beeword.word[0] for beeword in data])
    return initials_set == pangram_set


def get_metadata(
    data: list[config.Beeword],
    required: str,
    allowed: str,
    dictionary: config.Dictionary,
    word_list: config.WordList,
) -> config.Metadata:
    return config.Metadata(
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
        and len(word) == (config.NUM_ALLOWED_LETTERS + config.NUM_REQUIRED_LETTERS)
    )
    return (is_pangram, is_perfect)


def get_beeword(
    word: str, required: str, allowed: str, dictionary: config.Dictionary
) -> config.Beeword:
    is_pangram, is_perfect = get_pangram_status(
        word=word, pangram_set=set(required + allowed)
    )
    return config.Beeword(
        word=word,
        length=len(word),
        initials=word[0:2],
        is_pangram=is_pangram,
        is_perfect=is_perfect,
        url=dictionary.url_template.render(word=word),
    )


def get_beewords(
    word_list: config.WordList,
    required_letter: str,
    allowed_letters: str,
    dictionary: config.Dictionary,
) -> config.OutputData:
    with open(word_list.file_name, mode="r") as f:
        words = [line.lower() for line in f.read().splitlines()]
    all_letters_set = set(required_letter + allowed_letters)
    beewords: list[config.Beeword] = []
    for this_word in words:
        if required_letter in this_word and len(this_word) >= config.MIN_WORD_LENGTH:
            this_word_as_set = set(this_word)
            if this_word_as_set.issubset(all_letters_set):
                beewords.append(
                    get_beeword(
                        word=this_word,
                        required=required_letter,
                        allowed=allowed_letters,
                        dictionary=dictionary,
                    )
                )
    beewords = sorted(beewords, key=lambda beeword: beeword.word)
    return config.OutputData(
        data=beewords,
        metadata=get_metadata(
            data=beewords,
            required=required_letter,
            allowed=allowed_letters,
            dictionary=dictionary,
            word_list=word_list,
        ),
    )


def get_beewords_grouped(
    word_list: config.WordList,
    required_letter: str,
    allowed_letters: str,
    grouping: list[str],
    dictionary: config.Dictionary,
) -> config.OutputData:
    beewords = get_beewords(
        word_list=word_list,
        required_letter=required_letter,
        allowed_letters=allowed_letters,
        dictionary=dictionary,
    )

    def get_group0_key(beeword: config.Beeword):
        return getattr(beeword, grouping[0])

    def get_group1_key(beeword: config.Beeword):
        return getattr(beeword, grouping[1])

    beewords_list = beewords.data
    grouped_word_data = {}
    for group0, data0 in groupby(
        sorted(beewords_list, key=get_group0_key), key=get_group0_key
    ):
        grouped_word_data[group0] = {}
        for group1, data1 in groupby(
            sorted(data0, key=get_group1_key), key=get_group1_key
        ):
            grouped_word_data[group0][group1] = [beeword for beeword in data1]

    return config.OutputData(data=grouped_word_data, metadata=beewords.metadata)
