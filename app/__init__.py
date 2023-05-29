import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..")))

from config import UPLOAD_IMAGE_PATH, MAX_CONTENT_LENGTH
from flask import Flask

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_IMAGE_PATH
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


@app.route("/")
def index():
    return {"message": "Hello World"}


# from flaskr.api import bp as api_bp
# app.register_blueprint(api_bp, url_prefix="/api")

from app import jenisDokumenRoute
from app import tableRoute
