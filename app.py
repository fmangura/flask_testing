from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension


boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dope'
app.debug = True

# debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# board = boggle_game.make_board()
# session['board'] = board

@app.route('/')
def make_board():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('boggle.html')

@app.route('/check-word')
def check_word():
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word( board, word)
    print(word)

    return jsonify({'result': response})

@app.route('/get-score', methods=['POST'])
def get_score():
    score = request.json['score']
    highscore = session.get('highscore', 0)
    plays = session.get('plays', 0)

    session['highscore'] = max(score, highscore)
    session['plays'] = plays + 1

    return jsonify({'highscore': highscore})




