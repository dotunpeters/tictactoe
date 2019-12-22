"""
The flask application package.
"""

from flask import Flask
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

import game.views