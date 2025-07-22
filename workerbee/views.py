import logging
from flask import (
    abort,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    Response,
    send_file,
    session,
    url_for,
)
from io import BytesIO

from .bee import get_groupings, get_beewords_cached, get_summaries_cached
from .constants import Consts
from .dictionaries import Dictionaries, WIKT
from .types import Summary, OutputData
from .utils import error_check, get_filename, write_to_buffer
from .wordlists import WordLists, SCOWL_DEFAULT_60

_logger = logging.getLogger(__name__)

ARG_DEFAULTS = {
    Consts.REQUIRED_LETTER: "c",
    Consts.ALLOWED_LETTERS: "evitpa",
    Consts.DICTIONARY: WIKT,
    Consts.WORD_LIST: SCOWL_DEFAULT_60,
    Consts.GROUPING: Consts.INITIALS,
    Consts.FILE_TYPE: Consts.JSON,
    Consts.SUMMARY_SORT: Consts.DESCENDING,
    Consts.SHOW_WORDS: True,
    Consts.WORD_SORT: Consts.ALPHABETICALLY,
}

# whitelist args for session updates
ALLOWED_ARGS = set(ARG_DEFAULTS.keys())


def update_session_args(request_args: dict) -> dict:
    session_args: dict = session.get(Consts.ARGS, {}).copy()
    _logger.debug(f"session args before update: {session_args}")
    if request_args:
        for key in request.args:
            if key in ALLOWED_ARGS:
                session_args[key] = request_args[key]
            else:
                abort(400)
        # to support more checkboxes add them to this list
        for this_checkbox in [Consts.SHOW_WORDS]:
            if (value := request_args.get(this_checkbox)) is not None:
                session_args[this_checkbox] = value.lower() in ("true", "on")
    _logger.debug(f"session args after update: {session_args}")
    return session_args


def init_routes(app: Flask) -> None:

    ### Middleware ###
    @app.before_request
    def before_request() -> None:  # type: ignore reportUnusedFunction
        session.setdefault(Consts.ARGS, ARG_DEFAULTS.copy())
        session[Consts.ARGS] = update_session_args(request.args)

    @app.route("/")
    def root():  # type: ignore reportUnusedFunction
        return redirect(url_for("help"))

    @app.route(f"/help")
    def help() -> str:  # type: ignore reportUnusedFunctio
        return render_template("help.html")

    @app.route("/about")
    def about() -> str:  # type: ignore reportUnusedFunction
        return render_template("about.html")

    ### Forms ###
    @app.route(f"/find-words", methods=["GET"])
    def find_words() -> str:  # type: ignore reportUnusedFunction
        return render_template("find_words.html")

    @app.route(f"/show-summaries", methods=["GET"])
    def show_summaries() -> str:  # type: ignore reportUnusedFunction
        return render_template("show_summaries.html")

    ### Partials and downloads ###
    @app.route(f"/find-words-results", methods=["GET"])
    def find_words_results() -> str:  # type: ignore reportUnusedFunction
        args = session[Consts.ARGS]
        output_data: OutputData | None = None
        if error_msg := error_check(args=args):
            flash(message=error_msg)
        else:
            output_data = get_beewords_cached(
                word_list=WordLists[args[Consts.WORD_LIST]],
                required_letter=args[Consts.REQUIRED_LETTER],
                allowed_letters=args[Consts.ALLOWED_LETTERS],
                grouping=args[Consts.GROUPING],
                dictionary=Dictionaries[args[Consts.DICTIONARY]],
            )
        return render_template(
            "_find_words_results.html",
            output_data=output_data,
            grouping=get_groupings(args[Consts.GROUPING]),
        )

    @app.route(f"/show-summaries-results", methods=["GET"])
    def show_summaries_results() -> str:  # type: ignore reportUnusedFunction
        args = session[Consts.ARGS]
        summaries: list[Summary] = []
        if error_msg := error_check(args=args):
            flash(message=error_msg)
        else:
            summaries = get_summaries_cached(
                required_letter=args[Consts.REQUIRED_LETTER],
                allowed_letters=args[Consts.ALLOWED_LETTERS],
                dictionary=Dictionaries[args[Consts.DICTIONARY]],
                word_sort=args[Consts.WORD_SORT],
                summary_sort=args[Consts.SUMMARY_SORT],
            )
        return render_template(
            "_show_summaries_results.html",
            summaries=summaries,
            dictionary=Dictionaries[args[Consts.DICTIONARY]],
        )

    @app.route("/get-file", methods=["GET"])
    def get_file() -> Response:  # type: ignore reportUnusedFunction
        args = session[Consts.ARGS]
        output_data = get_beewords_cached(
            word_list=WordLists[args[Consts.WORD_LIST]],
            required_letter=args[Consts.REQUIRED_LETTER],
            allowed_letters=args[Consts.ALLOWED_LETTERS],
            dictionary=Dictionaries[args[Consts.DICTIONARY]],
            grouping=Consts.NO_GROUPING,
        )
        buffer = write_to_buffer(
            output_data=output_data,
            file_type=args[Consts.FILE_TYPE],
            grouping=args[Consts.GROUPING],
        )
        return send_file(
            BytesIO(buffer.getvalue().encode(encoding="utf-8")),
            download_name=get_filename(
                metadata=output_data.metadata,
                file_type=args[Consts.FILE_TYPE],
            ),
            as_attachment=True,
        )
