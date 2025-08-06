Worker Bee has a simple structure to make it useful as a learning tool.

- Flask application framework for web app (see `wsgi.py`, `__init__.py`, `views.py`)
- Flask views return html only. No json.
- Some simple javascript in frontend. Nothing fancy. No javascript framework
- No database. Backend word lists are in text files, loaded into memory on startup
- Ready for deployment with 
    - `systemd` - see `workerbee.service` and `workerbee.env.example` files
    - gunicorn - see `workerbee.service` for command line, env setup, etc
    - nginx reverse proxy - see server config in `alanjohnston.me`
- Simple manual `deploy.sh` script. No CI/CD.
- CLI implementation - see `__main__.py` (Does not use Flask run)
