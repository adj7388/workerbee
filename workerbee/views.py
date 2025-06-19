from . import app
from . import config as cfg
from .utils import error_check, get_filename, write_to_buffer
from .bee import get_beewords, get_beewords_grouped, get_groupings
from flask import request, session, redirect, flash, g, make_response, send_file, abort
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
            cfg.SHOW_WORDS: False,
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
    return cfg.JINJA_ENV.get_template(cfg.HOME_TEMPLATE).render(
        args=session.get(cfg.USER_ARGS, None),
        dictionaries=cfg.Dictionaries,
        word_lists=cfg.WordLists,
    )


@app.route(f"/{cfg.HELP_VIEW}/")
def help():
    if request.args:
        abort(400)
    return cfg.JINJA_ENV.get_template(cfg.HELP_TEMPLATE).render()


@app.route(f"/{cfg.ABOUT_VIEW}/")
def about():
    if request.args:
        abort(400)
    return cfg.JINJA_ENV.get_template(cfg.ABOUT_TEMPLATE).render()


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
        return cfg.JINJA_ENV.get_template(cfg.LISTWORDS_TEMPLATE).render(
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
        return cfg.JINJA_ENV.get_template(cfg.BEEWORDS_TEMPLATE).render(
            beeword_data=beewords.data,
            metadata=beewords.metadata,
            grouping=grouping,
        )


@app.route(f"/{cfg.SUMMARY_FORM_VIEW}", methods=["GET"])
def summary_form():
    if request.args:
        abort(400)
    return cfg.JINJA_ENV.get_template(cfg.SUMMARY_FORM_TEMPLATE).render(
        word_lists=cfg.WordLists,
        dictionaries=cfg.Dictionaries,
    )


@app.route(f"/{cfg.SUMMARY_VIEW}", methods=["GET"])
def summary():
    args_copy: dict = dict(request.args)
    args_copy[cfg.SHOW_WORDS] = request.args.get(cfg.SHOW_WORDS)
    args_copy[cfg.WORD_SORT] = request.args.get(cfg.WORD_SORT)
    args = session[cfg.USER_ARGS] = add_args_to_session(args_copy)
    error_msg = error_check(args=args)
    if error_msg:
        flash(message=error_msg)
        return redirect(f"/{cfg.SUMMARY_VIEW}")
    summary: list[cfg.OutputData] = []
    for word_list in cfg.WordLists.values():
        output_data = get_beewords(
            word_list=word_list,
            required_letter=args[cfg.REQUIRED_LETTER],
            allowed_letters=args[cfg.ALLOWED_LETTERS],
            dictionary=cfg.Dictionaries[cfg.MW],
        )
        summary.append(output_data)
    return cfg.JINJA_ENV.get_template(cfg.SUMMARY_TEMPLATE).render(
        summary=sorted(
            summary,
            key=lambda output_data: output_data.metadata.num_beewords,
            reverse=(True if args[cfg.SUMMARY_SORT] == "descending" else False),
        ),
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
