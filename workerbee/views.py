from collections import defaultdict

from . import app
from . import constants as const
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
    user_args = dict(session.get(const.ARGS, {}))
    for k, v in request_args.items():
        user_args[k] = v
    return user_args


@app.before_request
def before_request():
    session.setdefault(
        const.ARGS,
        {
            const.REQUIRED_LETTER: "a",
            const.ALLOWED_LETTERS: "cptive",
            const.DICTIONARY: dicts.WIKT,
            const.WORD_LIST: wordlists.SCOWL_DEFAULT_60,
            const.GROUPING: const.INITIALS,
            const.FILE_TYPE: const.JSON,
            const.SUMMARY_SORT: const.DESCENDING,
            const.SHOW_WORDS: const.SHOW_WORDS,
            const.WORD_SORT: const.ALPHABETICALLY,
        },
    )
    if (
        app.config[const.PROFILING] is True
        and const.PROFILE_REQUEST_ARG in request.args
    ):
        g.profiler = Profiler()
        g.profiler.start()


@app.after_request
def after_request(response):
    if app.config[const.PROFILING] is True and hasattr(g, "profiler"):
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


@app.route(f"/{const.BEEWORD_VIEW}", methods=["GET"])
def beewords():
    session[const.ARGS] = add_args_to_session(request.args)
    error_msg = error_check(args=session[const.ARGS])
    if error_msg:
        flash(message=error_msg)
        return redirect("home")
    if session[const.ARGS][const.GROUPING] == const.NO_GROUPING:
        beewords = get_beewords(
            word_list=wordlists.WordLists[session[const.ARGS][const.WORD_LIST]],
            required_letter=session[const.ARGS][const.REQUIRED_LETTER],
            allowed_letters=session[const.ARGS][const.ALLOWED_LETTERS],
            dictionary=dicts.Dictionaries[session[const.ARGS][const.DICTIONARY]],
        )
        return render_template(
            "listwords.html",
            beeword_list=beewords.data,
            metadata=beewords.metadata,
        )
    else:
        grouping = get_groupings(session[const.ARGS][const.GROUPING])
        beewords = get_beewords_grouped(
            word_list=wordlists.WordLists[session[const.ARGS][const.WORD_LIST]],
            required_letter=session[const.ARGS][const.REQUIRED_LETTER],
            allowed_letters=session[const.ARGS][const.ALLOWED_LETTERS],
            grouping=grouping,
            dictionary=dicts.Dictionaries[session[const.ARGS][const.DICTIONARY]],
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
        return beeword.length if word_sort == const.BYWORDLENGTH else beeword.word[0]

    reshaped: list[types.OutputData] = []
    for output in output_data:
        new_data = defaultdict(list)
        saved_key = get_key(
            beeword=output.data[0], word_sort=session[const.ARGS][const.WORD_SORT]
        )
        for beeword in output.data:
            this_key = get_key(beeword, word_sort=session[const.ARGS][const.WORD_SORT])
            saved_key = this_key if saved_key != this_key else saved_key
            new_data[this_key].append(beeword)
        reshaped.append(types.OutputData(data=new_data, metadata=output.metadata))
    return sorted(
        reshaped,
        key=lambda output_data: output_data.metadata.num_beewords,
        reverse=(
            True if session[const.ARGS][const.SUMMARY_SORT] == "descending" else False
        ),
    )


@app.route(f"/{const.SUMMARY_VIEW}", methods=["GET"])
def summary():
    user_args: dict = dict(request.args)
    user_args[const.SHOW_WORDS] = request.args.get(const.SHOW_WORDS)
    if user_args[const.SHOW_WORDS]:
        user_args[const.WORD_SORT] = request.args.get(const.WORD_SORT)
    session[const.ARGS] = add_args_to_session(user_args)
    error_msg = error_check(args=session[const.ARGS])
    if error_msg:
        flash(message=error_msg)
        return redirect("/summary_form")
    summary: list[types.OutputData] = []
    for word_list in wordlists.WordLists.values():
        output_data = get_beewords(
            word_list=word_list,
            required_letter=session[const.ARGS][const.REQUIRED_LETTER],
            allowed_letters=session[const.ARGS][const.ALLOWED_LETTERS],
            dictionary=dicts.Dictionaries[session[const.ARGS][const.DICTIONARY]],
        )
        summary.append(output_data)
    reshaped = reshape_for_summaries(output_data=summary)
    return render_template(
        "summary.html",
        summary=reshaped,
    )


@app.route(f"/{const.GETFILE_VIEW}/", methods=["GET"])
def getfile():
    session[const.ARGS] = add_args_to_session(request_args=request.args)
    if session[const.ARGS][const.GROUPING] == const.NO_GROUPING:
        output_data = get_beewords(
            word_list=wordlists.WordLists[session[const.ARGS][const.WORD_LIST]],
            required_letter=session[const.ARGS][const.REQUIRED_LETTER],
            allowed_letters=session[const.ARGS][const.ALLOWED_LETTERS],
            dictionary=dicts.Dictionaries[session[const.ARGS][const.DICTIONARY]],
        )
    else:
        output_data = get_beewords_grouped(
            word_list=wordlists.WordLists[session[const.ARGS][const.WORD_LIST]],
            required_letter=session[const.ARGS][const.REQUIRED_LETTER],
            allowed_letters=session[const.ARGS][const.ALLOWED_LETTERS],
            grouping=get_groupings(session[const.ARGS][const.GROUPING]),
            dictionary=dicts.Dictionaries[session[const.ARGS][const.DICTIONARY]],
        )
    buffer = write_to_buffer(
        output_data=output_data, file_type=session[const.ARGS][const.FILE_TYPE]
    )
    return send_file(
        BytesIO(buffer.getvalue().encode(encoding="utf-8")),
        download_name=get_filename(
            metadata=output_data.metadata,
            file_type=session[const.ARGS][const.FILE_TYPE],
        ),
        as_attachment=True,
    )
