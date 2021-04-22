import random
import os
import math
from collections import Counter

def roll_n_die(n: int) -> list:
    """
    simulate rolling the dice 3 times
    """
    dice = []
    for i in range(n):
        dice.append(random.randint(1, 6))
    dice.sort()
    return dice

def score_die(dice: list) -> tuple:
    """
    return the score of the dice and dice remaining
    """
    pts = 0
    # check for triples
    c = Counter(dice)
    triples = []
    seen = set()
    for i, j in c.items():
        if j >= 3:
            triples.append(i)
            if i not in seen:
                if i == 1:
                    pts += 1000
                else:
                    pts += i * 100
            seen.add(i)
    for elem in triples:
        for i in range(3):
            dice.remove(elem)
    rest = []
    while 1 in dice or 5 in dice:
        if dice[-1] == 1:
            pts += 100
            dice.pop()
        elif dice[-1] == 5:
            pts += 50
            dice.pop()
        else:
            rest.append(dice.pop())
    return (pts, len(rest) + len(dice))

def findbeststratA(num_of_games: str, other_player_stops_at=500):
    stopscores_to_winratio = {}
    for stopscore in range(50, 900, 50):
        res = simulate_2stratAplayers(
            int(num_of_games), int(other_player_stops_at), stopscore
        )
        stopscores_to_winratio[stopscore] = res["b"]
        # print(f'Stopping at {stopscore}: gives a win ratio of: {res["b"]}')
    return stopscores_to_winratio

def findbeststratB(num_of_games: str, stopdice1=2):
    # find the best strategy for B
    stopscores_to_winratio = {}
    for stopdice in range(0, 7):
        res = simulate_2stratBplayers(int(num_of_games), int(stopdice1), stopdice)
        stopscores_to_winratio[stopdice] = res["b"]
        # print(f'Stopping at {stopscore}: gives a win ratio of: {res["b"]}')
    return stopscores_to_winratio

def simulate(num_games: int) -> dict:
    count_ = 0
    win_counts = {}
    g = BotGame()
    for player in g.getPlayers():
        win_counts[str(int(player.getName()) + 1)] = 0
    while count_ < num_games:
        g = BotGame()
        for player in g.playGame():
            win_counts[str(int(player.getName()) + 1)] += 1
        count_ += 1
    for player in g.getPlayers():
        win_counts[str(int(player.getName()) + 1)] /= count_
    return win_counts

def simulate_2stratAplayers(num_games: str, up_to1: str, up_to2: str) -> dict:
    num_games = int(num_games)
    up_to1 = int(up_to1)
    up_to2 = int(up_to2)
    count_ = 0
    win_counts = {"a": 0, "b": 0}
    while count_ < num_games:
        g = BotGame(score_to_stop_at_each_turn=[up_to1, up_to2])
        for winner in g.playGame():
            # print(winner.getName())
            if int(winner.getName()) == 0:
                win_counts["a"] += 1
            else:
                win_counts["b"] += 1
        count_ += 1
    win_counts["a"] /= count_
    win_counts["b"] /= count_
    return win_counts

def simulate_stratABplayers(num_games: str, upto1: str, dicetostopat2: str) -> dict:
    num_games = int(num_games)
    count_ = 0
    player_A = BotPlayer(name="0", score_to_stop_at_each_turn=int(upto1), strategy="A")
    player_B = BotPlayer(name="1", stop_at_n_dice=int(dicetostopat2), strategy="B")
    win_counts = {"a": 0, "b": 0}
    while count_ < num_games:
        g = BotGame(playersToAdd=[player_A, player_B])
        for winner in g.playGame():
            if int(winner.getName()) == 0:
                win_counts["a"] += 1
            else:
                win_counts["b"] += 1
        count_ += 1
    win_counts["a"] /= count_
    win_counts["b"] /= count_
    return win_counts

def simulate_2stratBplayers(num_games: str, dicetostopat1: str, dicetostopat2: str):
    num_games = int(num_games)
    count_ = 0
    player_A = BotPlayer(name="0", stop_at_n_dice=int(dicetostopat1), strategy="B")
    player_B = BotPlayer(name="1", stop_at_n_dice=int(dicetostopat2), strategy="B")
    win_counts = {"a": 0, "b": 0}
    while count_ < num_games:
        g = BotGame(playersToAdd=[player_A, player_B])
        for winner in g.playGame():
            if int(winner.getName()) == 0:
                win_counts["a"] += 1
            else:
                win_counts["b"] += 1
        count_ += 1
    win_counts["a"] /= count_
    win_counts["b"] /= count_
    return win_counts

class BotGame:
    def __init__(
        self,
        num_of_players_to_generate=0,
        ending_score=10000,
        score_to_stop_at_each_turn=[],
        playersToAdd=[],
    ):
        random.seed(os.urandom(16))
        if score_to_stop_at_each_turn:
            self.num_of_players = len(score_to_stop_at_each_turn)
        else:
            self.num_of_players = 2
        self.ending_score = ending_score
        self.isFinalRound = False
        self.highestScore = -math.inf
        self.round = 0
        self.winners = []
        self.game_over = False
        self.verbose = False
        if not playersToAdd:
            self.players = []
            for i in range(self.num_of_players):
                self.players.append(
                    BotPlayer(
                        ending_score=ending_score,
                        name=str(i),
                        score_to_stop_at_each_turn=score_to_stop_at_each_turn[i],
                    )
                )
        else:
            self.players = playersToAdd
        for player in self.players:
            player.reset()

    def __next__(self):
        self.round += 1
        # if self.isFinalRound:
        #   Final round is set to have each player run until they either beat the current or get 0
        for i in range(self.num_of_players):
            next(self.players[i])
        for i in range(self.num_of_players):
            if self.players[i].getScore() > self.ending_score:
                self.game_over = True
                if self.verbose:
                    print("Game over in __next__")
                self.winners.append(self.players[i])
                self.highestScore = max(self.highestScore, self.players[i].getScore())
        if self.verbose:
            self.scoreboard()
        return self.round

    def playGame(self):
        winners = []
        while not self.game_over:
            next(self)
        for w in self.winners:
            if w.getScore() == self.highestScore:
                if self.verbose:
                    print(
                        f"Player {int(w.playerName)+1} won with {w.getScore()} points"
                    )
                winners.append(w)
        return winners

    def getPlayers(self):
        return self.players

    def getWinners(self):
        return self.winners

    def scoreboard(self):
        print("Scoreboard")
        print("=" * 20)
        for i in range(self.num_of_players):
            print(f"Player {i+1} has {self.players[i].getScore()} points")

class BotPlayer:
    def __init__(
        self,
        score_to_stop_at_each_turn=500,
        ending_score=10000,
        name="p1",
        num_dice=6,
        stop_at_n_dice=None,
        strategy=None,
    ):
        """
        add more strategies for computer to use
        """
        self.verbose = False
        self.score = 0
        self.turns = 0
        self.num_of_dice = num_dice
        self.playerName = name
        self.score_to_stop_at_turn = score_to_stop_at_each_turn
        self.game_end_score = ending_score
        self.game_over = False
        self.minNum_of_dice = stop_at_n_dice
        if strategy == None:
            if self.minNum_of_dice != None:
                self.strategy = "B"
            else:
                self.strategy = "A"
        else:
            self.strategy = strategy

    def reset(self):
        self.score = 0
        self.turns = 0
        self.game_over = False

    def __next__(self):
        """
        strategy: continues rolling until a number is reached
        takes all dice possible
        i.e. takes 3 5s rather than 1 5
        """
        score = 0
        num_of_dice = self.num_of_dice
        if self.game_over:
            if self.verbose:
                print("Game over")
            return score
        if self.score >= self.game_end_score and not self.game_over:
            if self.verbose:
                print(f"{self.score} >= {self.game_end_score}")
            self.game_over = True
        if self.strategy == "A":
            if self.verbose:
                print(f"Strategy A: roll until {self.score_to_stop_at_turn} is reached")
            while num_of_dice > 0 and score < self.score_to_stop_at_turn:
                if self.verbose:
                    print(f"{self.playerName} rolled {num_of_dice} dice")
                if self.verbose:
                    print(f"{self.playerName}'s score is {score}")
                dice_rolled = roll_n_die(num_of_dice)
                if self.verbose:
                    print(f"{self.playerName} rolled {dice_rolled}")
                pts, remaining = score_die(dice_rolled)
                if pts == 0:
                    if self.verbose:
                        print(f"{self.playerName}'s turn ended with 0 points")
                    return 0
                elif remaining == 0 and pts != 0:
                    if self.verbose:
                        print("All dice were used so rolling over")
                    num_of_dice = self.num_of_dice
                else:
                    score += pts
                    num_of_dice = remaining
            self.score += score
            if self.verbose:
                print(f"{score} is above {self.score_to_stop_at_turn}")
            return score
        elif self.strategy == "B":
            if self.verbose:
                print(f"Strategy B: roll until only {self.minNum_of_dice} dice left")
            while num_of_dice > self.minNum_of_dice and num_of_dice > 0:
                if self.verbose:
                    print(f"{self.playerName} rolled {num_of_dice} dice")
                if self.verbose:
                    print(f"{self.playerName}'s score is {score}")
                dice_rolled = roll_n_die(num_of_dice)
                if self.verbose:
                    print(f"{self.playerName} rolled {dice_rolled}")
                pts, remaining = score_die(dice_rolled)
                if pts == 0:
                    if self.verbose:
                        print(f"{self.playerName}'s turn ended with 0 points")
                    return 0
                elif remaining == 0 and pts != 0:
                    if self.verbose:
                        print("All dice were used so rolling over")
                    num_of_dice = self.num_of_dice
                else:
                    score += pts
                    num_of_dice = remaining
            self.score += score
            if self.verbose:
                print(f"Ending score {score}")
            if self.verbose:
                print(
                    f"{num_of_dice} less than or equal to the minimum number {self.minNum_of_dice}"
                )
            return score
        elif self.strategy == "C":
            if self.verbose:
                print(
                    f"Strategy C: ignore triple 5, roll until {self.score_to_stop_at_turn} is reached"
                )
            return score

    def getScore(self):
        return self.score

    def getName(self):
        return self.playerName

class UserPlayer:
    def __init__(self, s=500, ws=10000, name="p1"):
        self.total_score = 0
        self.round_score = 0
        self.turns = 0
        self.num_of_dice = 6
        self.playerName = name
        self.game_end_score = ws
        self.rolled_die = []
        self.game_over = False

    def roll(self):
        print(f'rolling {self.num_of_dice}')
        die_rolled = roll_n_die(self.num_of_dice)
        self.rolled_die = die_rolled
        return die_rolled
        
    def process_roll(self, die_to_take, end_turn):
        pts, rem = score_die(die_to_take)
        self.round_score += pts
        self.num_of_dice -= len(dice_to_take)
        self.num_of_dice += rem
        if not end_turn:
            print(f'{self.num_of_dice} left to roll')
        else:
            self.num_of_dice = 6
            self.total_score += self.round_score
            self.round_score = 0
        

    def getScore(self):
        return self.score
    
    def gameOver(self):
        return self.game_over
    
if __name__ == "__main__":
    # logic for user input -> rewrite for the front-end
    u = UserPlayer()
    while not u.gameOver():
        die_rolled = u.roll()
        print(f'You rolled: {die_rolled}')
        print('List of dice to take(i.e. 1,2,3): ')
        die_to_score = str(input()).split(',')
        print('Do you want to end your turn(y/n)?')
        endturn = 'y' in str(input())
        u.process_roll(die_to_score, endturn)
        
        
    
