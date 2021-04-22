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
    return render_template(
        "form3inputs.html",
        title="Home",
        form_title="Simulate 2 players who roll until they reach a certain score each turn",
        label1="Score for player 1 to stop at each turn",
        label2="Score for player 2 to stop at each turn",
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
            "textResults.html",
            new_text=str(res),
            num_games=num_games,
            player1_stoppingscore=player1_stoppingscore,
            player2_stoppingscore=player2_stoppingscore,
        )
    return render_template(
        "form3inputs.html",
        title="Home",
        form_title="Simulate a player who rolls until they have a certain amount of dice each turn against one who rolls until they reach a certain score each turn",
        label1="Score for player 1 to stop at each turn",
        label2="Number of dice for player 2 to stop at each turn",
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
            "textResults.html",
            new_text=str(res),
            num_games=num_games,
            player1_stoppingscore=player1_stoppingscore,
            player2_stoppingscore=player2_stoppingscore,
        )
    return render_template(
        "form3inputs.html",
        title="Home",
        form_title="Simulate 2 players who roll until they have a certain amount of dice each turn",
        label1="Number of dice for player 1 to stop at each turn",
        label2="Number of dice for player 2 to stop at each turn",
    )


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
    msg = ''
    if request.method == "POST":
        resp = request.form.getlist('hello')
        resp = list(map(lambda x: int(x), resp))
        if len(resp)==0:
                msg = 'You must choose a dice'
                return render_template(
                    "demoResults.html",
                    num_dice=cache['remaining'],
                    res=['rolled_die'],
                    die=cache['die'],
                    total_score=cache['user_score_total'],
                    pts=cache['user_score_round'],
                    round=cache['current_round'],
                    message=msg,
                )
        if request.form.getlist('end'):
            # tell user their turn ended
            msg += 'You ended your turn'
            print('You ended your turn')
            # add score for the round
            pts_round, _ = dicethousand.score_die(resp)
            cache['user_score_round'] += pts_round
            cache['user_score_total'] += cache['user_score_round']
            # roll for computer and save it to list to display to the use
            # set the score for the next round to 0
            cache['user_score_round'] = 0
            cache['current_round'] += 1
            cache['remaining'] = 6
        else:
            resp = list(map(lambda x: int(x), resp))
            pts_round, r = dicethousand.score_die(resp)
            print(f'resp: {resp}, remaining: {cache["remaining"]}')
            cache['remaining'] -= len(resp)
            cache['remaining'] += r
            print(f'remaining: {cache["remaining"]}')
            if pts_round == 0:
                # turn is over and there are no points for this round
                print('Turn is over')
                msg += 'Turn is over and all points were lost for the round :('
                # roll for computer and save it to list to display to the use
                # set the score for the next round
                cache['user_score_round'] = 0
                cache['remaining'] = 6
                cache['current_round'] += 1
            elif cache['remaining'] == 0 and pts_round!=0:
                print('All dice used, rollover')
                # roll over points
                cache['remaining'] = 6
                cache['user_score_round'] += pts_round
            else:
                cache['user_score_round'] += pts_round
        remaining = cache['remaining']
        rolled_die = dicethousand.roll_n_die(remaining)
        die = [i for i in range(1, cache['remaining']+1)]
        cache['die'] = die
        return render_template(
                "demoResults.html",
                num_dice=cache['remaining'],
                res=rolled_die,
                die=die,
                total_score=cache['user_score_total'],
                pts=cache['user_score_round'],
                round=cache['current_round'],
                message=msg,
                )
    cache = {'remaining': 6, 'rolled_die': 0, 'die': [], 'user_score_round': 0, 'user_score_total': 0, 'computer_score_round': 0, 'computer_score_total': 0, 'current_round': 0}
    return render_template(
        "demoResults.html",
        num_dice=6,
        res = dicethousand.roll_n_die(6),
        die=[1, 2, 3, 4, 5, 6],
        total_score=0,
        pts=0,
        round=cache['current_round'],
        message='Beginning a new game'
    )
    
# @app.route("/demoResults")


