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


# Pig latin page, when we click translate, moves to text result page
@app.route("/text", methods=["GET", "POST"])
def text():
    if request.method == "POST":
        res = dicethousand.simulate_2stratAplayers(request.form['num_games'], request.form['player1_stoppingscore'], request.form['player2_stoppingscore'])
        return render_template(
            "textResults.html", new_text=str(res)
        )
    return render_template("text.html", title="Home")
