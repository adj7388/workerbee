import flask
import os

app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRETBEEKEY")

# Importing here sets up routes as a side effect
from . import views  # pyright: ignore
