try:
    from flask import (
        render_template,
        redirect,
        url_for,
        request,
        send_from_directory,
        flash,
    )
except:
    print("Make sure to pip install Flask twilio")
from app import app
import os

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from app import dicethousand

# Home page, renders the index.html template
@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", title="Home")


# play 2 strategy A players
@app.route("/AA", methods=["GET", "POST"])
def text():
    if request.method == "POST":
        num_games = request.form["num_games"]
        player1_stoppingscore = request.form["player1_stoppingscore"]
        player2_stoppingscore = request.form["player2_stoppingscore"]
        res = dicethousand.simulate_2stratAplayers(
            num_games, player1_stoppingscore, player2_stoppingscore
        )
        return render_template(
            "textResults.html",
            new_text=str(res),
            num_games=num_games,
            player1_stoppingscore=player1_stoppingscore,
            player2_stoppingscore=player2_stoppingscore,
        )
    return render_template("form3inputs.html", title="Home")


# strategy A vs strategy B who wins!
@app.route("/AB", methods=["GET", "POST"])
def text2():
    if request.method == "POST":
        num_games = request.form["num_games"]
        player1_stoppingscore = request.form["player1_stoppingscore"]
        player2_stoppingscore = request.form["player2_stoppingscore"]
        res = dicethousand.simulate_stratABplayers(
            num_games, player1_stoppingscore, player2_stoppingscore
        )
        return render_template(
            "textResults.html",
            new_text=str(res),
            num_games=num_games,
            player1_stoppingscore=player1_stoppingscore,
            player2_stoppingscore=player2_stoppingscore,
        )
    return render_template("form3inputs.html", title="Home")


# 2 strategy B players face off
@app.route("/BB", methods=["GET", "POST"])
def text3():
    if request.method == "POST":
        num_games = request.form["num_games"]
        player1_stoppingscore = request.form["player1_stoppingscore"]
        player2_stoppingscore = request.form["player2_stoppingscore"]
        res = dicethousand.simulate_stratABplayers(
            num_games, player1_stoppingscore, player2_stoppingscore
        )
        return render_template(
            "textResults.html",
            new_text=str(res),
            num_games=num_games,
            player1_stoppingscore=player1_stoppingscore,
            player2_stoppingscore=player2_stoppingscore,
        )
    return render_template("form3inputs.html", title="Home")


@app.route("/bestA", methods=["GET", "POST"])
def text4():
    if request.method == "POST":
        num_games = request.form["num_games"]
        player1_stoppingscore = request.form["player1_stoppingscore"]
        if player1_stoppingscore:
            res = dicethousand.findbeststratA(num_games, player1_stoppingscore)
        else:
            res = dicethousand.findbeststratA(num_games)
        return render_template(
            "textResults.html",
            new_text=str(res),
            num_games=num_games,
            player1_stoppingscore=player1_stoppingscore,
        )
    return render_template("form3inputs.html", title="Home")


@app.route("/bestB", methods=["GET", "POST"])
def text5():
    if request.method == "POST":
        num_games = request.form["num_games"]
        player1_stoppingscore = request.form["player1_stoppingscore"]
        if player1_stoppingscore:
            res = dicethousand.findbeststratB(num_games, player1_stoppingscore)
        else:
            res = dicethousand.findbeststratB(num_games)
        return render_template(
            "textResults.html",
            new_text=str(res),
            num_games=num_games,
            player1_stoppingscore=player1_stoppingscore,
        )
    return render_template("form3inputs.html", title="Home")
