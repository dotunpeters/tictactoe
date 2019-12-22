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

"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, session, url_for, redirect
from game.minimax import minimax, winner
from game import app


@app.route('/')
def home():
    if "board" not in session:
        session['board'] = [[None for i in range(6)] for j in range(6) ]
        session['turn'] = "X"
        session['all_moves'] = []
        session['winner'] = None
        session['draw'] = 0

    return render_template(
        'index.html',
        title='TicTacToe',
        year=datetime.now().year,
        board=session['board'],
        turn=session['turn'],
        winner=session['winner'],
        draw=session['draw']
    )

@app.route('/play/<int:row>/<int:col>')
def play(row, col):
    session['board'][col][row] = "X"
    session['all_moves'].append(("X", row, col))
    session['winner'] = winner("X", session['board'])
    if session['winner'] == "X":
        return redirect(url_for("home"))
    if session['draw'] == True:
        return redirect(url_for("home"))

    col, row = minimax(session['board'])
    session['board'][col][row] = "O"
    session['all_moves'].append(("O", row, col))
    session['winner'] = winner("O", session['board'])
    if session['winner'] == "O":
        return redirect(url_for("home"))
    if session['draw'] == True:
        return redirect(url_for("home"))

    return redirect(url_for("home"))

@app.route('/refresh')
def refresh():
    session['board'] = [[None for i in range(6)] for j in range(6) ]
    session['winner'] = None
    return redirect(url_for("home"))

@app.route('/undo')
def undo():
    for _ in range(2):
        try:
            pop = session['all_moves'].pop()
        except IndexError:
            return redirect(url_for("home"))
        turn, row, col = pop
        session['board'][col][row] = None
    return redirect(url_for("home"))

