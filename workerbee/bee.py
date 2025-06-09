from itertools import groupby
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


def check_bingo(data: list[dict], pangram_set: set) -> bool:
    initials_set = set([word[config.WORD][0] for word in data])
    return initials_set == pangram_set


def get_metadata(
    data: list,
    required: str,
    allowed: str,
    dictionary: config.Dictionary,
    word_list: config.WordList,
) -> dict:
    return {
        config.NUM_BEEWORDS: len(data),
        config.REQUIRED_LETTER: required,
        config.ALLOWED_LETTERS: allowed,
        config.BINGO: check_bingo(data, set(required + allowed)),
        config.PERFECT_PANGRAMS: [
            beeword for beeword in data if beeword[config.IS_PERFECT]
        ],
        config.NONPERFECT_PANGRAMS: [
            beeword
            for beeword in data
            if beeword[config.IS_PANGRAM] and not beeword[config.IS_PERFECT]
        ],
        config.DICTIONARY: dictionary.name,
        config.WORD_LIST: word_list.name,
        config.BEEWORD_FIELDNAMES: list(data[0].keys()) if data else '',
    }


def get_pangram_status(word: str, pangram_set: set) -> tuple:
    is_pangram = bool(set(word) == pangram_set)
    is_perfect = bool(
        is_pangram
        and len(word) == (config.NUM_ALLOWED_LETTERS + config.NUM_REQUIRED_LETTERS)
    )
    return (is_pangram, is_perfect)


def get_beeword(
    word: str, required: str, allowed: str, dictionary: config.Dictionary
) -> dict:
    is_pangram, is_perfect = get_pangram_status(
        word=word, pangram_set=set(required + allowed)
    )
    return {
        config.WORD: word,
        config.LENGTH: len(word),
        config.INITIALS: word[0:2],
        config.IS_PANGRAM: is_pangram,
        config.IS_PERFECT: is_perfect,
        config.URL: dictionary.url_template.render(word=word),
    }


def get_beewords(
    word_list: config.WordList,
    required_letter: str,
    allowed_letters: str,
    dictionary: config.Dictionary,
) -> dict:
    with open(word_list.file_name, mode="r") as f:
        words = [line.lower() for line in f.read().splitlines()]
    all_letters_set = set(required_letter + allowed_letters)
    beewords = []
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
    return_dict = dict()
    return_dict[config.DATA] = sorted(
        beewords, key=lambda beeword: beeword[config.WORD]
    )
    return_dict[config.METADATA] = get_metadata(
        data=beewords,
        required=required_letter,
        allowed=allowed_letters,
        dictionary=dictionary,
        word_list=word_list,
    )
    return return_dict


def get_beewords_grouped(
    word_list: config.WordList,
    required_letter: str,
    allowed_letters: str,
    grouping: list[str],
    dictionary: config.Dictionary,
) -> dict:
    beewords = get_beewords(
        word_list=word_list,
        required_letter=required_letter,
        allowed_letters=allowed_letters,
        dictionary=dictionary,
    )

    def get_group0_key(beeword):
        return beeword[grouping[0]]

    def get_group1_key(beeword):
        return beeword[grouping[1]]

    beewords_list = beewords[config.DATA]
    grouped_word_data = {}
    for group0, data0 in groupby(
        sorted(beewords_list, key=get_group0_key), key=get_group0_key
    ):
        grouped_word_data[group0] = {}
        for group1, data1 in groupby(
            sorted(data0, key=get_group1_key), key=get_group1_key
        ):
            grouped_word_data[group0][group1] = [beeword for beeword in data1]

    return_dict = {}
    return_dict[config.DATA] = grouped_word_data
    return_dict[config.METADATA] = beewords[config.METADATA]
    return return_dict
