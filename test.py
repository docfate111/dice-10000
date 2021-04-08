import random
import os
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


class BotGame:
    def __init__(self, num_of_players=2, ending_score=10000):
        random.seed(os.urandom(16))
        self.num_of_players = num_of_players
        self.ending_score = ending_score
        self.player_scores = {}
        self.players = []
        self.isFinalRound = False
        self.winners = []
        for i in range(num_of_players):
            self.players.append(BotPlayer(ending_score=ending_score, name=str(i)))
            self.player_scores[str(i)] = 0

    def __next__(self):
        if self.isFinalRound:
            """
            Final round is set to have each player run until they either beat the current or get 0
            """
        for i in range(self.num_of_players):
            self.player_scores[str(i)] += next(self.players[i])
        for i in range(self.num_of_players):
            if self.player_scores[str(i)] > self.ending_score:
                self.isFinalRound = True
                self.winners.append(str(i))
        self.scoreboard()

    def scoreboard(self):
        print("Scoreboard")
        print("=" * 20)
        for i in range(self.num_of_players):
            print(f"Player {i+1} has {self.player_scores[str(i)]} points")


class BotPlayer:
    def __init__(
        self, score_to_stop_at_each_turn=500, ending_score=10000, name="p1", num_dice=6
    ):
        """
        add more strategies for computer to use
        """
        self.score = 0
        self.turns = 0
        self.num_of_dice = num_dice
        self.playerName = name
        self.score_to_stop_at_turn = score_to_stop_at_each_turn
        self.game_end_score = ending_score

    def __iter__(self):
        return self

    def __next__(self):
        """
        strategy: continues rolling until a number is reached
        takes all dice possible
        i.e. takes 3 5s rather than 1 5
        """
        score = 0
        num_of_dice = self.num_of_dice
        if self.score >= self.game_end_score:
            print(f"{self.score} >= {self.game_end_score}")
            raise StopIteration
        while num_of_dice > 0 and score < self.score_to_stop_at_turn:
            print(f"{self.playerName} rolled {num_of_dice} dice")
            dice_rolled = roll_n_die(num_of_dice)
            print(f"{self.playerName} rolled {dice_rolled}")
            pts, remaining = score_die(dice_rolled)
            if pts == 0:
                print(f"{self.playerName}'s turn ended with 0 points")
                return 0
            elif remaining == 0 and pts != 0:
                print("All dice were used so rolling over")
                num_of_dice = self.num_of_dice
            else:
                score += pts
                num_of_dice = remaining
        self.score += score
        print(f"{score} is above {self.score_to_stop_at_turn}")
        return score

    def getScore(self):
        return self.score


class UserPlayer:
    def __init__(self, s=500, ws=10000, name="p1"):
        """
        add more strategies for computer to use
        """
        self.score = 0
        self.turns = 0
        self.num_of_dice = 6
        self.playerName = name
        self.score_to_stop_at_turn = s
        self.game_end_score = ws

    def __next__(self, num_of_dice):
        """
        does a simple role
        TODO: create other functions to interact with user
        """
        dice_rolled = roll_n_die(num_of_dice)
        return score_die(dice_rolled)

    def getScore(self):
        return self.score


# logic for user input -> rewrite for the front-end
# print('Do you want to end your turn(y/n)?')
#                 resp = str(input())
#                 if 'y' in resp or 'Y' in resp:
#                     print('Ending your turn')
#                     self.score += pts
#                     return pts
#                 while True:
#                     print('How many die to use in the next roll?')
#                     n = int(input())
#                     if n < 1:
#                         print('Invalid choice. Try again')
#                     else:
#                         break
#                 for i in range(n):
#                     print(f'Removing dice {i+1} of {n}\nPrint number to remove:')
#                     x = int(input())
#                     if x in dice_rolled:
#                         dice_rolled.remove(x)
#                     else:
#                         print('Choice not in dice')
#                 pts, remaining = score_die(dice_rolled)

if __name__ == "__main__":
    g = BotGame()
    print(next(g))
