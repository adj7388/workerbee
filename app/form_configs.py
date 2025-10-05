from flask import url_for
from typing import Any

from .constants import Consts

#### lowerCamelCase used for keys because configs used mainly in javascript


def get_find_words_config() -> dict[str, Any]:
    return {
        "formId": "findWordsSearchForm",
        "url": url_for("find_words_results"),
        "resultsContainerId": Consts.RESULTS_CONTAINER_ID,
    }


def get_show_summaries_config() -> dict[str, Any]:
    return {
        "formId": "summarySearchForm",
        "url": url_for("show_summaries_results"),
        "resultsContainerId": Consts.RESULTS_CONTAINER_ID,
    }


def get_display_changes_config() -> dict[str, Any]:
    return {
        "changesCheckboxId": Consts.DISPLAY_CHANGES,
        "changesContainerId": "displayChangesContainer",
        "updateSessionUrl": url_for(Consts.DISPLAY_CHANGES),
    }


def get_form_history_config(form_id: str) -> dict[str, Any]:
    return {
        "formId": form_id,
        "resultsContainerId": Consts.RESULTS_CONTAINER_ID,
        "backId": "backBtn",
        "forwardId": "forwardBtn",
        "indexId": "indexDisplay",
        "saveId": "saveHistoryBtn",
        "deleteId": "deleteHistoryBtn",
    }


def get_show_words_config() -> dict[str, Any]:
    return {
        "showWordsId": Consts.SHOW_WORDS,
        "alphabeticallyId": Consts.ALPHABETICALLY,
        "byWordLengthId": Consts.BYWORDLENGTH,
    }
