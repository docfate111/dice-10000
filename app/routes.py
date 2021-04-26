import copy

cpy = lambda x: copy.deepcopy(x)
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
            "graph.html",
            labels=[i for i in range(1, len(res)+1)],
            values=res,
            values2=[100-i for i in res],
            player1_stoppingscore=player1_stoppingscore,
            player2_stoppingscore=player2_stoppingscore,
            player1_label="Player A rolled until they scored: ",
            player2_label="Player B rolled until they scored: "
        )
    return render_template(
        "form3inputs.html",
        title="Home",
        form_title="Simulate 2 players who roll until they reach a certain score each turn",
        label1="Score for player A to stop at each turn",
        label2="Score for player B to stop at each turn",
    )


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
            "graph.html",
            labels=[i for i in range(1, len(res)+1)],
            values=res,
            values2=[100-i for i in res],
            player1_stoppingscore=player1_stoppingscore,
            player2_stoppingscore=str(player2_stoppingscore)+" dice",
            player1_label="Player A rolled until they scored: ",
            player2_label="Player B rolled until they had: "
        )
    return render_template(
        "form3inputs.html",
        title="Home",
        form_title="Simulate a player who rolls until they have a certain amount of dice each turn against one who rolls until they reach a certain score each turn",
        label1="Score for player A to stop at each turn",
        label2="Number of dice for player B to stop at each turn",
    )


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
            "graph.html",
            labels=[i for i in range(1, len(res)+1)],
            values=res,
            values2=[100-i for i in res],
            player1_stoppingscore=str(player1_stoppingscore)+" dice remaining",
            player2_stoppingscore=str(player2_stoppingscore)+" dice remaining",
            player1_label="Player A rolled until they had: ",
            player2_label="Player B rolled until they had: "
        )
    return render_template(
        "form3inputs.html",
        title="Home",
        form_title="Simulate 2 players who roll until they have a certain amount of dice each turn",
        label1="Number of dice for player A to stop at each turn",
        label2="Number of dice for player B to stop at each turn",
    )


# strategy AB vs A
# simulate_2stratBvsABplayers(50, 1, 4, 350)
# 2 strategy B players face off
@app.route("/stratBvsAB", methods=["GET", "POST"])
def textP():
    if request.method == "POST":
        num_games = request.form["num_games"]
        p1dice = request.form["player1_dicestop"]
        p2dice = request.form["player2_dicestop"]
        p2score = request.form["player2_score"]
        res = dicethousand.simulate_2stratBvsABplayers(
            num_games, p1dice, p2dice, p2score
        )
        return render_template(
            "graph.html",
            labels=[i for i in range(1, len(res)+1)],
            values=res,
            values2=[100-i for i in res],
            player1_stoppingscore=str(p1dice)+" dice remaining",
            player2_stoppingscore=str(p2dice)+" dice remaining",
            player1_label="Player A rolled until they had: ",
            player2_label="Player B rolled until they either scored "+ str(p2score) + " or had: "
        )
    return render_template(
        "form4inputs.html",
        title="Home",
        form_title="Simulate 2 players who roll until they have a certain amount of dice each turn",
        label1="Number of dice for player A to stop at each turn",
        label2="Number of dice for player B to stop at each turn",
        label3="Player B score to stop at each turn",
    )


@app.route("/stratAvsAB", methods=["GET", "POST"])
def textQ():
    if request.method == "POST":
        num_games = request.form["num_games"]
        scoretostopat1 = request.form["player1_dicestop"]
        dicetostopat2 = request.form["player2_dicestop"]
        score_to_stop_at_turn = request.form["player2_score"]
        res = dicethousand.simulate_2stratAvsABplayers(
            num_games, scoretostopat1, dicetostopat2, score_to_stop_at_turn
        )
        return render_template(
            "graph.html",
            labels=[i for i in range(1, len(res)+1)],
            values=res,
            values2=[100-i for i in res],
            player1_stoppingscore=scoretostopat1,
            player2_stoppingscore=str(dicetostopat2)+" dice remaining",
            player1_label="Score for player A to stop rolling at:  ",
            player2_label="Player B rolled until they either scored "+ str(score_to_stop_at_turn) + " or had less than "
        )
    return render_template(
        "form4inputs.html",
        title="Home",
        form_title="Simulate 2 players who roll until they have a certain amount of dice each turn",
        label1="Score for player A to stop rolling at: ",
        label2="Number of dice for player B to stop at each turn",
        label3="Player B score to stop at each turn",
    )
    
# strategy AB vs AB
# BotPlayer(name="0", score_to_stop_at_each_turn=350, stop_at_n_dice=4, strategy="AB")


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
    return render_template(
        "form2inputs.html",
        title="Home",
        form_title="Simulate several games to find the best score to stop at for each turn (based on your opponent)",
        label1="(Optional) Stopping score for player 1",
    )


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
    return render_template(
        "form2inputs.html",
        title="Home",
        form_title="Simulate several games to find the best number of dice to stop at for each turn (based on your opponent)",
        label1="(Optional) Number of dice for player 1",
    )


@app.route("/rules", methods=["GET"])
def text6():
    return render_template(
        "rules.html",
    )


cache = {}


@app.route("/demo", methods=["GET", "POST"])
def text7():
    global cache
    if request.method == "POST" and "player" in cache.keys():
        resp = request.form.getlist("hello")
        resp = list(map(lambda x: int(x), resp))
        u, die_rolled, not_crap_out = dicethousand.game_func_roll(cache["player"])
        cache["not_crap_out"] = not_crap_out
        cache["current_round"] += 1
        not_endturn = True
        if request.form.getlist("end"):
            not_endturn = False
        u, c, comp_rolled = dicethousand.game_func_input(
            cpy(u), cpy(cache["computer"]), resp, not_crap_out, not_endturn
        )
        cache["player"] = cpy(u)
        cache["computer"] = cpy(c)
        return render_template(
            "demoResults.html",
            num_dice=cache["player"].getNumDice(),
            die_rolled=die_rolled,
            die=[1, 2, 3, 4, 5, 6],
            total_score=u.getTotalScore(),
            pts=u.getRoundScore(),
            round=cache["current_round"],
            message="message goes here",
            computer_rolled=comp_rolled,
            computer_score=cache["computer"].getScore(),
        )
    cache["computer"] = cpy(
        dicethousand.LoudBotPlayer(
            name="0", score_to_stop_at_each_turn=350, stop_at_n_dice=4, strategy="AB"
        )
    )
    cache["player"] = cpy(dicethousand.UserPlayer())
    u, die_rolled, not_crap_out = dicethousand.game_func_roll(cache["player"])
    cache["not_crap_out"] = not_crap_out
    cache["current_round"] = 1
    cache["player"] = cpy(u)
    return render_template(
        "demoResults.html",
        num_dice=6,
        die_rolled=die_rolled,
        die=[1, 2, 3, 4, 5, 6],
        total_score=u.getTotalScore(),
        pts=u.getRoundScore(),
        round=cache["current_round"],
        message="Beginning a new game",
        computer_rolled=0,
        computer_score=cache["computer"].getScore(),
    )


@app.route("/graphtest")
def text8():
    data = [
        ('a', 2),
        ('b', 3),
        ('c', 4)
    ]
    labels = [row[0] for row in data]
    vals = [row[1] for row in data]
    return render_template('graph.html', labels=labels, values=vals)
