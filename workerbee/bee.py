from collections import defaultdict
from dataclasses import asdict
from itertools import groupby

from . import cache
from .constants import Consts
from .dictionaries import Dictionary
from .types import (
    SpellingBeeWord,
    Metadata,
    NestedSpellingBeeWords,
    FindWordsOutput,
    ShowSummariesOutput,
    PangramStatus,
)
from .wordlists import WordList, WordLists


def _check_bingo(data: list[SpellingBeeWord], pangram_set: set) -> bool:
    initials_set = set([beeword.word[0] for beeword in data])
    return initials_set == pangram_set


def _get_metadata(
    data: list[SpellingBeeWord],
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


def _get_pangram_status(word: str, pangram_set: set) -> PangramStatus:
    is_pangram = bool(set(word) == pangram_set)
    is_perfect = bool(is_pangram and (len(word) == len(pangram_set)))
    return PangramStatus(
        is_pangram=is_pangram,
        is_perfect=is_perfect,
    )


def _get_beeword(
    word: str, pangram_set: set, dictionary: Dictionary
) -> SpellingBeeWord:
    pangram_status: PangramStatus = _get_pangram_status(
        word=word,
        pangram_set=pangram_set,
    )
    return SpellingBeeWord(
        word=word,
        length=len(word),
        initials=word[0:2],
        is_pangram=pangram_status.is_pangram,
        is_perfect=pangram_status.is_perfect,
        definition_url=dictionary.url_template.render(word=word),
    )


def _get_beewords(
    word_list: WordList,
    required_letter: str,
    allowed_letters: str,
    dictionary: Dictionary,
) -> list[SpellingBeeWord]:
    all_letters_set = set(required_letter + allowed_letters)
    beewords: list[SpellingBeeWord] = []
    for this_word in word_list.words:  # type: ignore
        if required_letter in this_word:
            if set(this_word).issubset(all_letters_set):
                beewords.append(
                    _get_beeword(
                        word=this_word,
                        pangram_set=all_letters_set,
                        dictionary=dictionary,
                    )
                )
    return sorted(beewords, key=lambda beeword: beeword.word)


def get_groupings(grouping: str) -> tuple[str, ...]:
    if grouping == Consts.LENGTH:
        return (Consts.LENGTH, Consts.INITIALS)
    elif grouping == Consts.INITIALS:
        return (Consts.INITIALS, Consts.LENGTH)
    elif grouping == Consts.NO_GROUPING:
        return (Consts.NO_GROUPING,)
    else:
        raise ValueError(f"Bad grouping: {grouping}")


def get_beewords(
    word_list: WordList,
    required_letter: str,
    allowed_letters: str,
    dictionary: Dictionary,
    grouping: str = Consts.NO_GROUPING,
) -> FindWordsOutput:
    beewords: list[SpellingBeeWord] = _get_beewords(
        word_list=word_list,
        required_letter=required_letter,
        allowed_letters=allowed_letters,
        dictionary=dictionary,
    )
    # for FindWordsOutput.nested, default to initials/length grouping
    grouping_list: tuple[str, ...] = (
        get_groupings(Consts.INITIALS)
        if grouping == Consts.NO_GROUPING
        else get_groupings(grouping)
    )

    def get_group0_key(beeword: SpellingBeeWord) -> str | int:
        return getattr(beeword, grouping_list[0])

    def get_group1_key(beeword: SpellingBeeWord) -> str | int:
        return getattr(beeword, grouping_list[1])

    nested_beewords: NestedSpellingBeeWords = {}
    for group0, data0 in groupby(
        sorted(beewords, key=get_group0_key), key=get_group0_key
    ):
        nested_beewords[group0] = {}
        for group1, data1 in groupby(
            sorted(data0, key=get_group1_key), key=get_group1_key
        ):
            nested_beewords[group0][group1] = [beeword for beeword in data1]

    return FindWordsOutput(
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


def get_beewords_cached(
    word_list: WordList,
    required_letter: str,
    allowed_letters: str,
    dictionary: Dictionary,
    grouping: str = Consts.NO_GROUPING,
) -> FindWordsOutput:

    findwords_cache = cache.get_cache(cache.FIND_WORDS)

    key = frozenset(
        (
            word_list.file_name,
            frozenset(allowed_letters),
            required_letter,
            grouping,
            dictionary.name,
        )
    )

    if cached := findwords_cache.get(key):
        return cached
    else:
        words = get_beewords(
            word_list=word_list,
            required_letter=required_letter,
            allowed_letters=allowed_letters,
            dictionary=dictionary,
            grouping=grouping,
        )
        findwords_cache.set(key, words)
        return words


def _convert_to_summaries(
    find_words_output: list[FindWordsOutput],
    word_sort: str,
    summary_sort: str,
) -> list[ShowSummariesOutput]:

    def get_key(beeword: SpellingBeeWord, sort_type: str) -> str | int:
        return beeword.length if sort_type == Consts.BYWORDLENGTH else beeword.word[0]

    summaries: list[ShowSummariesOutput] = []
    for output in find_words_output:
        beeword_dict = defaultdict(list[SpellingBeeWord])
        saved_key = get_key(
            beeword=output.flat[0],
            sort_type=word_sort,
        )
        for beeword in output.flat:
            this_key = get_key(beeword, sort_type=word_sort)
            saved_key = this_key if saved_key != this_key else saved_key
            beeword_dict[this_key].append(beeword)
        summaries.append(
            ShowSummariesOutput(beewords=beeword_dict, metadata=output.metadata)
        )
    return sorted(
        summaries,
        key=lambda summary: summary.metadata.num_beewords,
        reverse=(True if summary_sort == "descending" else False),
    )


def get_summaries(
    required_letter: str,
    allowed_letters: str,
    dictionary: Dictionary,
    word_sort: str,
    summary_sort: str,
    grouping: str = Consts.NO_GROUPING,
) -> list[ShowSummariesOutput]:
    output_list: list[FindWordsOutput] = []
    for word_list in WordLists.values():
        find_words_output = get_beewords(
            word_list=word_list,
            required_letter=required_letter,
            allowed_letters=allowed_letters,
            dictionary=dictionary,
            grouping=grouping,
        )
        output_list.append(find_words_output)
    return _convert_to_summaries(
        find_words_output=output_list,
        word_sort=word_sort,
        summary_sort=summary_sort,
    )


def get_summaries_cached(
    required_letter: str,
    allowed_letters: str,
    word_sort: str,
    summary_sort: str,
    dictionary: Dictionary,
    grouping: str = Consts.NO_GROUPING,
) -> list[ShowSummariesOutput]:

    summaries_cache = cache.get_cache(cache.SHOW_SUMMARIES)

    key = frozenset(
        (
            required_letter,
            frozenset(allowed_letters),
            summary_sort,
            word_sort,
            dictionary.name,
        )
    )

    if cached_summaries := summaries_cache.get(key):
        return cached_summaries
    else:
        summaries = get_summaries(
            required_letter=required_letter,
            allowed_letters=allowed_letters,
            word_sort=word_sort,
            summary_sort=summary_sort,
            dictionary=dictionary,
            grouping=grouping,
        )
        summaries_cache.set(key, summaries)
        return summaries
