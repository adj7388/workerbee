from collections import defaultdict

from . import app
from .constants import Consts
from . import dictionaries as dicts
from . import types
from . import wordlists
from .utils import error_check, get_filename, write_to_buffer
from .bee import get_beewords, get_beewords_grouped, get_groupings
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


def add_args_to_session(request_args):
    user_args = dict(session.get(Consts.ARGS, {}))
    for k, v in request_args.items():
        user_args[k] = v
    return user_args


@app.before_request
def before_request():
    session.setdefault(
        Consts.ARGS,
        {
            Consts.REQUIRED_LETTER: "a",
            Consts.ALLOWED_LETTERS: "cptive",
            Consts.DICTIONARY: dicts.WIKT,
            Consts.WORD_LIST: wordlists.SCOWL_HUGE_80,
            Consts.GROUPING: Consts.INITIALS,
            Consts.FILE_TYPE: Consts.JSON,
            Consts.SUMMARY_SORT: Consts.DESCENDING,
            Consts.SHOW_WORDS: Consts.SHOW_WORDS,
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


@app.route("/home")
def home():
    if request.args:
        abort(400)
    return render_template("home.html")


@app.route(f"/help")
def help():
    if request.args:
        abort(400)
    return render_template("help.html")


@app.route("/about")
def about():
    if request.args:
        abort(400)
    return render_template("about.html")


@app.route(f"/{Consts.BEEWORD_VIEW}", methods=["GET"])
def beewords():
    session[Consts.ARGS] = add_args_to_session(request.args)
    error_msg = error_check(args=session[Consts.ARGS])
    if error_msg:
        flash(message=error_msg)
        return redirect("home")
    if session[Consts.ARGS][Consts.GROUPING] == Consts.NO_GROUPING:
        beewords = get_beewords(
            word_list=wordlists.WordLists[session[Consts.ARGS][Consts.WORD_LIST]],
            required_letter=session[Consts.ARGS][Consts.REQUIRED_LETTER],
            allowed_letters=session[Consts.ARGS][Consts.ALLOWED_LETTERS],
            dictionary=dicts.Dictionaries[session[Consts.ARGS][Consts.DICTIONARY]],
        )
        return render_template(
            "listwords.html",
            beeword_list=beewords.data,
            metadata=beewords.metadata,
        )
    else:
        grouping = get_groupings(session[Consts.ARGS][Consts.GROUPING])
        beewords = get_beewords_grouped(
            word_list=wordlists.WordLists[session[Consts.ARGS][Consts.WORD_LIST]],
            required_letter=session[Consts.ARGS][Consts.REQUIRED_LETTER],
            allowed_letters=session[Consts.ARGS][Consts.ALLOWED_LETTERS],
            grouping=grouping,
            dictionary=dicts.Dictionaries[session[Consts.ARGS][Consts.DICTIONARY]],
        )
        return render_template(
            "beewords.html",
            beeword_data=beewords.data,
            metadata=beewords.metadata,
            grouping=grouping,
        )


@app.route("/summary_form", methods=["GET"])
def summary_form():
    if request.args:
        abort(400)
    return render_template("summary_form.html")


def reshape_for_summaries(
    output_data: list[types.OutputData],
) -> list[types.OutputData]:

    def get_key(beeword: types.Beeword, word_sort: str):
        return beeword.length if word_sort == Consts.BYWORDLENGTH else beeword.word[0]

    reshaped: list[types.OutputData] = []
    for output in output_data:
        new_data = defaultdict(list)
        saved_key = get_key(
            beeword=output.data[0], word_sort=session[Consts.ARGS][Consts.WORD_SORT]
        )
        for beeword in output.data:
            this_key = get_key(
                beeword, word_sort=session[Consts.ARGS][Consts.WORD_SORT]
            )
            saved_key = this_key if saved_key != this_key else saved_key
            new_data[this_key].append(beeword)
        reshaped.append(types.OutputData(data=new_data, metadata=output.metadata))
    return sorted(
        reshaped,
        key=lambda output_data: output_data.metadata.num_beewords,
        reverse=(
            True if session[Consts.ARGS][Consts.SUMMARY_SORT] == "descending" else False
        ),
    )


@app.route(f"/{Consts.SUMMARY_VIEW}", methods=["GET"])
def summary():
    user_args: dict = dict(request.args)
    user_args[Consts.SHOW_WORDS] = request.args.get(Consts.SHOW_WORDS)
    if user_args[Consts.SHOW_WORDS]:
        user_args[Consts.WORD_SORT] = request.args.get(Consts.WORD_SORT)
    session[Consts.ARGS] = add_args_to_session(user_args)
    error_msg = error_check(args=session[Consts.ARGS])
    if error_msg:
        flash(message=error_msg)
        return redirect("/summary_form")
    summary: list[types.OutputData] = []
    for word_list in wordlists.WordLists.values():
        output_data = get_beewords(
            word_list=word_list,
            required_letter=session[Consts.ARGS][Consts.REQUIRED_LETTER],
            allowed_letters=session[Consts.ARGS][Consts.ALLOWED_LETTERS],
            dictionary=dicts.Dictionaries[session[Consts.ARGS][Consts.DICTIONARY]],
        )
        summary.append(output_data)
    reshaped = reshape_for_summaries(output_data=summary)
    return render_template(
        "summary.html",
        summary=reshaped,
    )


@app.route(f"/{Consts.GETFILE_VIEW}/", methods=["GET"])
def getfile():
    session[Consts.ARGS] = add_args_to_session(request_args=request.args)
    if session[Consts.ARGS][Consts.GROUPING] == Consts.NO_GROUPING:
        output_data = get_beewords(
            word_list=wordlists.WordLists[session[Consts.ARGS][Consts.WORD_LIST]],
            required_letter=session[Consts.ARGS][Consts.REQUIRED_LETTER],
            allowed_letters=session[Consts.ARGS][Consts.ALLOWED_LETTERS],
            dictionary=dicts.Dictionaries[session[Consts.ARGS][Consts.DICTIONARY]],
        )
    else:
        output_data = get_beewords_grouped(
            word_list=wordlists.WordLists[session[Consts.ARGS][Consts.WORD_LIST]],
            required_letter=session[Consts.ARGS][Consts.REQUIRED_LETTER],
            allowed_letters=session[Consts.ARGS][Consts.ALLOWED_LETTERS],
            grouping=get_groupings(session[Consts.ARGS][Consts.GROUPING]),
            dictionary=dicts.Dictionaries[session[Consts.ARGS][Consts.DICTIONARY]],
        )
    buffer = write_to_buffer(
        output_data=output_data, file_type=session[Consts.ARGS][Consts.FILE_TYPE]
    )
    return send_file(
        BytesIO(buffer.getvalue().encode(encoding="utf-8")),
        download_name=get_filename(
            metadata=output_data.metadata,
            file_type=session[Consts.ARGS][Consts.FILE_TYPE],
        ),
        as_attachment=True,
    )
