@app.before_request
def before_request():
    session.setdefault(
        config.USER_ARGS,
        {
            config.REQUIRED_LETTER: "u",
            config.ALLOWED_LETTERS: "ncdeli",
            config.DICTIONARY: config.WIKT,
            config.WORD_LIST: config.SCOWL_DEFAULT_60,
            config.SUMMARY_SORT: config.DESCENDING,
            config.SHOW_WORDS: config.SHOW_WORDS,
            config.GROUPING: config.INITIALS,
            config.FILE_TYPE: config.JSON,
        },
    )
    if config.PROFILING is True and config.PROFILE_REQUEST_ARG in request.args:
        g.profiler = Profiler()
        g.profiler.start()


def save_to_session(**request_args):
    user_args = dict(session.get(config.USER_ARGS, {}))
    for k, v in request_args.items():
        user_args[k] = v
    session[config.USER_ARGS] = user_args
    return user_args
