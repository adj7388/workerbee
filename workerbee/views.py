from collections import defaultdict

from . import app
from . import config as cfg
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
    user_args = dict(session.get(cfg.USER_ARGS, {}))
    for k, v in request_args.items():
        user_args[k] = v
    return user_args


@app.before_request
def before_request():
    session.setdefault(
        cfg.USER_ARGS,
        {
            cfg.REQUIRED_LETTER: "u",
            cfg.ALLOWED_LETTERS: "ncdeli",
            cfg.DICTIONARY: cfg.WIKT,
            cfg.WORD_LIST: cfg.SCOWL_DEFAULT_60,
            cfg.GROUPING: cfg.INITIALS,
            cfg.FILE_TYPE: cfg.JSON,
            cfg.SUMMARY_SORT: cfg.DESCENDING,
            cfg.SHOW_WORDS: True,
            cfg.WORD_SORT: cfg.ALPHABETICALLY,
        },
    )
    if cfg.PROFILING is True and cfg.PROFILE_REQUEST_ARG in request.args:
        g.profiler = Profiler()
        g.profiler.start()


@app.after_request
def after_request(response):
    if cfg.PROFILING is True and hasattr(g, "profiler"):
        g.profiler.stop()
        output_html = g.profiler.output_html()
        return make_response(output_html)
    else:
        return response


@app.route("/")
def home():
    if request.args:
        abort(400)
    return render_template(
        cfg.HOME_TEMPLATE,
        args=session.get(cfg.USER_ARGS, None),
        dictionaries=cfg.Dictionaries,
        word_lists=cfg.WordLists,
    )


@app.route(f"/{cfg.HELP_VIEW}/")
def help():
    if request.args:
        abort(400)
    return render_template(cfg.HELP_TEMPLATE)


@app.route(f"/{cfg.ABOUT_VIEW}/")
def about():
    if request.args:
        abort(400)
    return render_template(cfg.ABOUT_TEMPLATE)


@app.route(f"/{cfg.BEEWORD_VIEW}", methods=["GET"])
def beewords():
    user_args = session[cfg.USER_ARGS] = add_args_to_session(request.args)
    error_msg = error_check(args=user_args)
    if error_msg:
        flash(message=error_msg)
        return redirect(cfg.HOME_VIEW)
    if user_args[cfg.GROUPING] == cfg.NO_GROUPING:
        beewords = get_beewords(
            word_list=cfg.WordLists[user_args[cfg.WORD_LIST]],
            required_letter=user_args[cfg.REQUIRED_LETTER],
            allowed_letters=user_args[cfg.ALLOWED_LETTERS],
            dictionary=cfg.Dictionaries[user_args[cfg.DICTIONARY]],
        )
        return render_template(
            cfg.LISTWORDS_TEMPLATE,
            beeword_list=beewords.data,
            metadata=beewords.metadata,
        )
    else:
        grouping = get_groupings(user_args[cfg.GROUPING])
        beewords = get_beewords_grouped(
            word_list=cfg.WordLists[user_args[cfg.WORD_LIST]],
            required_letter=user_args[cfg.REQUIRED_LETTER],
            allowed_letters=user_args[cfg.ALLOWED_LETTERS],
            grouping=grouping,
            dictionary=cfg.Dictionaries[user_args[cfg.DICTIONARY]],
        )
        return render_template(
            cfg.BEEWORDS_TEMPLATE,
            beeword_data=beewords.data,
            metadata=beewords.metadata,
            grouping=grouping,
        )


@app.route(f"/{cfg.SUMMARY_FORM_VIEW}", methods=["GET"])
def summary_form():
    if request.args:
        abort(400)
    return render_template(cfg.SUMMARY_FORM_TEMPLATE)


def reshape_for_summaries(
    output_data: list[cfg.OutputData],
) -> list[cfg.OutputData]:

    def get_key(beeword: cfg.Beeword, word_sort: str):
        return beeword.length if word_sort == cfg.LENGTH else beeword.word[0]

    word_sort = (
        cfg.LENGTH
        if session[cfg.USER_ARGS][cfg.WORD_SORT] == cfg.BYWORDLENGTH
        else cfg.ALPHABETICALLY
    )
    reshaped: list[cfg.OutputData] = []
    for output in output_data:
        new_data = defaultdict(list)
        saved_key = get_key(beeword=output.data[0], word_sort=word_sort)
        for beeword in output.data:
            this_key = get_key(beeword, word_sort=word_sort)
            saved_key = this_key if saved_key != this_key else saved_key
            new_data[this_key].append(beeword)
        reshaped.append(cfg.OutputData(data=new_data, metadata=output.metadata))
    return sorted(
        reshaped,
        key=lambda output_data: output_data.metadata.num_beewords,
        reverse=(
            True if session[cfg.USER_ARGS][cfg.SUMMARY_SORT] == "descending" else False
        ),
    )


@app.route(f"/{cfg.SUMMARY_VIEW}", methods=["GET"])
def summary():
    user_args: dict = dict(request.args)
    user_args[cfg.SHOW_WORDS] = request.args.get(cfg.SHOW_WORDS)
    if user_args[cfg.SHOW_WORDS]:
        user_args[cfg.WORD_SORT] = request.args.get(cfg.WORD_SORT)
    user_args = session[cfg.USER_ARGS] = add_args_to_session(user_args)
    error_msg = error_check(args=user_args)
    if error_msg:
        flash(message=error_msg)
        return redirect(f"/{cfg.SUMMARY_FORM_VIEW}")
    summary: list[cfg.OutputData] = []
    for word_list in cfg.WordLists.values():
        output_data = get_beewords(
            word_list=word_list,
            required_letter=user_args[cfg.REQUIRED_LETTER],
            allowed_letters=user_args[cfg.ALLOWED_LETTERS],
            dictionary=cfg.Dictionaries[session[cfg.USER_ARGS][cfg.DICTIONARY]],
        )
        summary.append(output_data)
    reshaped = reshape_for_summaries(output_data=summary)
    return render_template(
        cfg.SUMMARY_TEMPLATE,
        summary=reshaped,
    )


@app.route(f"/{cfg.GETFILE_VIEW}/", methods=["GET"])
def getfile():
    user_args = session[cfg.USER_ARGS] = add_args_to_session(request_args=request.args)
    if user_args[cfg.GROUPING] == cfg.NO_GROUPING:
        output_data = get_beewords(
            word_list=cfg.WordLists[user_args[cfg.WORD_LIST]],
            required_letter=user_args[cfg.REQUIRED_LETTER],
            allowed_letters=user_args[cfg.ALLOWED_LETTERS],
            dictionary=cfg.Dictionaries[user_args[cfg.DICTIONARY]],
        )
    else:
        output_data = get_beewords_grouped(
            word_list=cfg.WordLists[user_args[cfg.WORD_LIST]],
            required_letter=user_args[cfg.REQUIRED_LETTER],
            allowed_letters=user_args[cfg.ALLOWED_LETTERS],
            grouping=get_groupings(user_args[cfg.GROUPING]),
            dictionary=cfg.Dictionaries[user_args[cfg.DICTIONARY]],
        )
    buffer = write_to_buffer(
        output_data=output_data, file_type=user_args[cfg.FILE_TYPE]
    )
    return send_file(
        BytesIO(buffer.getvalue().encode(encoding="utf-8")),
        download_name=get_filename(
            metadata=output_data.metadata,
            file_type=user_args[cfg.FILE_TYPE],
        ),
        as_attachment=True,
    )
