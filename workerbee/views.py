from flask import (
    Response,
    render_template,
    session,
    flash,
    g,
    request,
    make_response,
    abort,
    redirect,
    send_file,
)
from io import BytesIO
from pyinstrument import Profiler

from . import app

from .bee import get_beewords, get_beewords_cached, get_groupings, get_summaries_cached
from .constants import Consts
from .dictionaries import Dictionaries, WIKT
from .types import Summary, OutputData
from .utils import error_check, get_filename, write_to_buffer
from .wordlists import WordLists, SCOWL_HUGE_80


def update_session_args(request_args: dict) -> dict:
    session_args: dict = session.get(Consts.ARGS, {}).copy()
    for k, v in request_args.items():
        session_args[k] = v
    # handle checkboxes
    for this_arg in [Consts.SHOW_WORDS]:
        if (value := request_args.get(this_arg)) is not None:
            session_args[this_arg] = value in ("true", "on")
    return session_args


@app.before_request
def before_request():
    session.setdefault(
        Consts.ARGS,
        {
            Consts.REQUIRED_LETTER: "c",
            Consts.ALLOWED_LETTERS: "evitpa",
            Consts.DICTIONARY: WIKT,
            Consts.WORD_LIST: SCOWL_HUGE_80,
            Consts.GROUPING: Consts.INITIALS,
            Consts.FILE_TYPE: Consts.JSON,
            Consts.SUMMARY_SORT: Consts.DESCENDING,
            Consts.SHOW_WORDS: True,
            Consts.WORD_SORT: Consts.ALPHABETICALLY,
        },
    )
    session[Consts.ARGS] = update_session_args(request.args)
    if (
        app.config[Consts.PROFILING] is True
        and Consts.PROFILE_REQUEST_ARG in request.args
    ):
        g.profiler = Profiler()
        g.profiler.start()


@app.after_request
def after_request(response):
    if app.config[Consts.PROFILING] is True and hasattr(g, "profiler"):
        g.profiler.stop()
        output_html = g.profiler.output_html()
        return make_response(output_html)
    else:
        return response


@app.route("/")
def root():
    return abort(400) if request.args else redirect("find-words")


@app.route(f"/help")
def help():
    return abort(400) if request.args else render_template("help.html")


@app.route("/about")
def about():
    return abort(400) if request.args else render_template("about.html")


@app.route(f"/find-words", methods=["GET"])
def find_words():
    return abort(400) if request.args else render_template("find_words.html")


@app.route(f"/find-words-results", methods=["GET"])
def find_words_results():
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


@app.route(f"/show-summaries", methods=["GET"])
def show_summaries():
    return abort(400) if request.args else render_template("show_summaries.html")


@app.route(f"/show-summaries-results", methods=["GET"])
def show_summaries_results():
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
def get_file() -> Response:
    args = session[Consts.ARGS]
    output_data = get_beewords(
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
