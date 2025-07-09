from collections import defaultdict
from flask import (
    render_template,
    session,
    g,
    request,
    make_response,
    abort,
    flash,
    redirect,
    send_file,
)
from io import BytesIO
from pyinstrument import Profiler

from . import app

from .bee import get_beewords, get_groupings
from .constants import Consts
from .dictionaries import Dictionaries, WIKT
from .types import Beeword, Summary, OutputData
from .utils import error_check, get_filename, write_to_buffer
from .wordlists import WordLists, SCOWL_HUGE_80


def handle_checkboxes(session_args, request_args) -> dict:
    for this_arg in [Consts.SHOW_WORDS]:
        value = request_args.get(this_arg, None)
        if value is not None:
            session_args[this_arg] = True if value in ["true", "on"] else False
    return session_args


def update_session_args(request_args) -> dict:
    session_args: dict = session.get(Consts.ARGS, {})
    for k, v in request_args.items():
        session_args[k] = v
    return handle_checkboxes(session_args, request_args)


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


def convert_to_summaries(
    output_data: list[OutputData],
) -> list[Summary]:

    def get_key(beeword: Beeword, sort_type: str) -> str | int:
        return beeword.length if sort_type == Consts.BYWORDLENGTH else beeword.word[0]

    summaries: list[Summary] = []
    for output in output_data:
        beeword_dict = defaultdict(list[Beeword])
        saved_key = get_key(
            beeword=output.flat[0],
            sort_type=session[Consts.ARGS][Consts.WORD_SORT],
        )
        for beeword in output.flat:
            this_key = get_key(
                beeword, sort_type=session[Consts.ARGS][Consts.WORD_SORT]
            )
            saved_key = this_key if saved_key != this_key else saved_key
            beeword_dict[this_key].append(beeword)
        summaries.append(Summary(beewords=beeword_dict, metadata=output.metadata))
    return sorted(
        summaries,
        key=lambda summary: summary.metadata.num_beewords,
        reverse=(
            True if session[Consts.ARGS][Consts.SUMMARY_SORT] == "descending" else False
        ),
    )


@app.route(f"/{Consts.GETFILE_VIEW}/", methods=["GET"])
def getfile():
    session[Consts.ARGS] = update_session_args(request.args)
    output_data = get_beewords(
        word_list=WordLists[session[Consts.ARGS][Consts.WORD_LIST]],
        required_letter=session[Consts.ARGS][Consts.REQUIRED_LETTER],
        allowed_letters=session[Consts.ARGS][Consts.ALLOWED_LETTERS],
        dictionary=Dictionaries[session[Consts.ARGS][Consts.DICTIONARY]],
        grouping=Consts.NO_GROUPING,
    )
    buffer = write_to_buffer(
        output_data=output_data,
        file_type=session[Consts.ARGS][Consts.FILE_TYPE],
        grouping=session[Consts.ARGS][Consts.GROUPING],
    )
    return send_file(
        BytesIO(buffer.getvalue().encode(encoding="utf-8")),
        download_name=get_filename(
            metadata=output_data.metadata,
            file_type=session[Consts.ARGS][Consts.FILE_TYPE],
        ),
        as_attachment=True,
    )


@app.route(f"/find-words", methods=["GET"])
def find_words():
    return abort(400) if request.args else render_template("find-words.html")


@app.route(f"/_findwords-results", methods=["GET"])
def findwords_results():
    session[Consts.ARGS] = update_session_args(request.args)
    error_msg = error_check(args=session[Consts.ARGS])
    if error_msg:
        flash(message=error_msg)
    output_data = get_beewords(
        word_list=WordLists[session[Consts.ARGS][Consts.WORD_LIST]],
        required_letter=session[Consts.ARGS][Consts.REQUIRED_LETTER],
        allowed_letters=session[Consts.ARGS][Consts.ALLOWED_LETTERS],
        grouping=session[Consts.ARGS][Consts.GROUPING],
        dictionary=Dictionaries[session[Consts.ARGS][Consts.DICTIONARY]],
    )
    return render_template(
        "_findwords_results.html",
        output_data=output_data,
        grouping=get_groupings(session[Consts.ARGS][Consts.GROUPING]),
    )


@app.route(f"/show-summaries", methods=["GET"])
def show_summaries():
    return abort(400) if request.args else render_template("show-summaries.html")


@app.route(f"/_summaries-results", methods=["GET"])
def summaries_results():
    session[Consts.ARGS] = update_session_args(request.args)
    error_msg = error_check(args=session[Consts.ARGS])
    summaries: list[Summary] = []
    if error_msg:
        flash(message=error_msg)
    else:
        output_list: list[OutputData] = []
        for word_list in WordLists.values():
            output_data = get_beewords(
                word_list=word_list,
                required_letter=session[Consts.ARGS][Consts.REQUIRED_LETTER],
                allowed_letters=session[Consts.ARGS][Consts.ALLOWED_LETTERS],
                dictionary=Dictionaries[session[Consts.ARGS][Consts.DICTIONARY]],
                grouping=Consts.NO_GROUPING,
            )
            output_list.append(output_data)
        summaries = convert_to_summaries(output_data=output_list)
    return render_template(
        "_showsummaries_results.html",
        summaries=summaries,
        dictionary=Dictionaries[session[Consts.ARGS][Consts.DICTIONARY]],
    )
