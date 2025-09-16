from flask import url_for
from typing import Any

from .constants import Consts

#### lowerCamelCase used for keys because configs used mainly in javascript


def get_find_words_config() -> dict[str, Any]:
    return {
        "formId": "findWordsSearchForm",
        "url": url_for("find_words_results"),
        "fieldKeys": [
            Consts.REQUIRED_LETTER,
            Consts.ALLOWED_LETTERS,
            Consts.GROUPING,
            Consts.WORD_LIST,
            Consts.DICTIONARY,
        ],
        "buttonLabels": {"first": "Find Words", "after": "Update Words"},
        "resultsContainerId": "results",
    }


def get_show_summaries_config() -> dict[str, Any]:
    return {
        "formId": "summarySearchForm",
        "url": url_for("show_summaries_results"),
        "fieldKeys": [
            Consts.REQUIRED_LETTER,
            Consts.ALLOWED_LETTERS,
            Consts.SUMMARY_SORT,
            Consts.SHOW_WORDS,
            Consts.DICTIONARY,
            Consts.WORD_SORT,
            "Word sort:",
        ],
        "buttonLabels": {"first": "Show Summaries", "after": "Update Summaries"},
        "resultsContainerId": "results",
    }


def get_display_changes_config() -> dict[str, Any]:
    return {
        "displayChangesId": Consts.DISPLAY_CHANGES,
        "displayChangesUrl": url_for(Consts.DISPLAY_CHANGES),
    }


def get_form_history_config(form_id: str, results_container_id: str) -> dict[str, Any]:
    return {
        "formId": form_id,
        "resultsContainerId": results_container_id,
        "backId": "backBtn",
        "forwardId": "forwardBtn",
        "indexId": "indexDisplay",
        "saveId": "saveHistoryBtn",
    }


def get_show_words_config() -> dict[str, Any]:
    return {
        "showWordsId": Consts.SHOW_WORDS,
        "alphabeticallyId": Consts.ALPHABETICALLY,
        "byWordLengthId": Consts.BYWORDLENGTH,
    }
