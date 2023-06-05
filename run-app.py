import os
import sys

__dir__ = os.path.dirname(__file__)
sys.path.append(__dir__)

from app import app

app.config.from_pyfile("../config.py")

if __name__ == "__main__":
    app.run(debug=True)
