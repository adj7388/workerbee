from . import app
from . import config
from .utils import error_check, get_filename, write_to_buffer
from .bee import get_beewords, get_beewords_grouped, get_groupings
from flask import request, session, redirect, flash, g, make_response, send_file, abort
from io import BytesIO
from pyinstrument import Profiler


@app.before_request
def before_request():
    if config.PROFILING is True and config.PROFILE_REQUEST_ARG in request.args:
        g.profiler = Profiler()
        g.profiler.start()


@app.after_request
def after_request(response):
    if config.PROFILING is True and hasattr(g, "profiler"):
        g.profiler.stop()
        output_html = g.profiler.output_html()
        return make_response(output_html)
    else:
        return response


@app.route("/")
def home():
    if request.args:
        abort(400)
    return config.JINJA_ENV.get_template(config.HOME_TEMPLATE).render(
        args=session.get(config.USER_ARGS, None),
        dictionaries=config.Dictionaries,
        word_lists=config.WordLists,
    )


@app.route(f"/{config.HELP_VIEW}/")
def help():
    if request.args:
        abort(400)
    return config.JINJA_ENV.get_template(config.HELP_TEMPLATE).render()


@app.route(f"/{config.ABOUT_VIEW}/")
def about():
    if request.args:
        abort(400)
    return config.JINJA_ENV.get_template(config.ABOUT_TEMPLATE).render()


@app.route(f"/{config.BEEWORD_VIEW}", methods=["GET"])
def beewords():
    if request.method == "GET":
        session[config.USER_ARGS] = request.args
        error_msg = error_check(args=session[config.USER_ARGS])
        if error_msg:
            flash(message=error_msg)
            return redirect(config.HOME_VIEW)
        if session[config.USER_ARGS][config.GROUPING] == config.NO_GROUPING:
            beewords = get_beewords(
                word_list=config.WordLists[session[config.USER_ARGS][config.WORD_LIST]],
                required_letter=session[config.USER_ARGS][config.REQUIRED_LETTER],
                allowed_letters=session[config.USER_ARGS][config.ALLOWED_LETTERS],
                dictionary=config.Dictionaries[
                    session[config.USER_ARGS][config.DICTIONARY]
                ],
            )
            return config.JINJA_ENV.get_template(config.LISTWORDS_TEMPLATE).render(
                beeword_list=beewords.data,
                metadata=beewords.metadata,
            )
        else:
            grouping = get_groupings(session[config.USER_ARGS][config.GROUPING])
            beewords = get_beewords_grouped(
                word_list=config.WordLists[session[config.USER_ARGS][config.WORD_LIST]],
                required_letter=session[config.USER_ARGS][config.REQUIRED_LETTER],
                allowed_letters=session[config.USER_ARGS][config.ALLOWED_LETTERS],
                grouping=grouping,
                dictionary=config.Dictionaries[
                    session[config.USER_ARGS][config.DICTIONARY]
                ],
            )
            return config.JINJA_ENV.get_template(config.BEEWORDS_TEMPLATE).render(
                beeword_data=beewords.data,
                metadata=beewords.metadata,
                grouping=grouping,
            )
    return config.JINJA_ENV.get_template(config.ERROR_TEMPLATE).render(
        message="Something went wrong"
    )


@app.route(f"/{config.SUMMARY_FORM_VIEW}", methods=["GET"])
def summary_form():
    if request.args:
        abort(400)
    return config.JINJA_ENV.get_template(config.SUMMARY_FORM_TEMPLATE).render(
        args=session.get(config.USER_ARGS, None),
        dictionaries=config.Dictionaries,
        word_lists=config.WordLists,
    )


@app.route(f"/{config.SUMMARY_VIEW}")
def summary():
    if request.method == "GET":
        session[config.USER_ARGS] = request.args
        error_msg = error_check(args=session[config.USER_ARGS])
        if error_msg:
            flash(message=error_msg)
            return redirect(f"/{config.SUMMARY_VIEW}")
    summary: list[config.OutputData] = []
    for word_list in config.WordLists.values():
        beewords = get_beewords(
            word_list=word_list,
            required_letter=session[config.USER_ARGS][config.REQUIRED_LETTER],
            allowed_letters=session[config.USER_ARGS][config.ALLOWED_LETTERS],
            dictionary=config.Dictionaries[config.MW],
        )
        summary.append(beewords)
    return config.JINJA_ENV.get_template(config.SUMMARY_TEMPLATE).render(
        summary=sorted(
            summary,
            key=lambda output_data: output_data.metadata.num_beewords,
            reverse=(
                True
                if session[config.USER_ARGS][config.SUMMARY_SORT] == "descending"
                else False
            ),
        ),
    )


@app.route(f"/{config.GETFILE_VIEW}/", methods=["GET"])
def getfile():
    saved_session = session.get(config.USER_ARGS, {})
    file_type = request.args.get(config.FILE_TYPE, config.TXT)
    session[config.FILE_TYPE] = file_type
    if saved_session[config.GROUPING] == config.NO_GROUPING:
        output_data = get_beewords(
            word_list=config.WordLists[saved_session[config.WORD_LIST]],
            required_letter=saved_session[config.REQUIRED_LETTER],
            allowed_letters=saved_session[config.ALLOWED_LETTERS],
            dictionary=config.Dictionaries[saved_session[config.DICTIONARY]],
        )
    else:
        output_data = get_beewords_grouped(
            word_list=config.WordLists[saved_session[config.WORD_LIST]],
            required_letter=saved_session[config.REQUIRED_LETTER],
            allowed_letters=saved_session[config.ALLOWED_LETTERS],
            grouping=get_groupings(saved_session[config.GROUPING]),
            dictionary=config.Dictionaries[saved_session[config.DICTIONARY]],
        )
    buffer = write_to_buffer(output_data=output_data, file_type=file_type)
    return send_file(
        BytesIO(buffer.getvalue().encode(encoding="utf-8")),
        download_name=get_filename(
            metadata=output_data.metadata,
            file_type=file_type,
        ),
        as_attachment=True,
    )
