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
    print(dice)
    return (pts, len(rest) + len(dice))


class Game:
    def __init__(self):
        random.seed(os.urandom(16))
        self.num_of_players = 2
        self.ending_score = 10000


class Player:
    def __init__(self, s=500, ws=10000, name="p1", user_input=False):
        self.score = 0
        self.turns = 0
        self.num_of_dice = 6
        self.playerName = name
        self.score_to_stop_at_turn = s
        self.game_end_score = ws
        self.user_input = user_input

    def __iter__(self):
        return self

    def __next__(self):
        # assuming score to stop at is the strategy
        # could also go by number of dice
        score = 0
        num_dice = self.num_of_dice
        if self.score >= self.game_end_score:
            raise StopIteration
        while num_dice > 0:
            dice_rolled = roll_n_die(6)
            print(f"{self.playerName} rolled {dice_rolled}")
            pts, remaining = score_die(dice_rolled)
            if self.user_input and pts > 0:
                print("do you want to end your turn(y/n)?")
                resp = str(input())
                if "y" in resp or "Y" in resp:
                    self.score += score
                    return score
                print("how many die to remove?")
                n = int(input())
                for i in range(n):
                    dice_rolled.remove(int(input()))
                pts, remaining = score_die(dice_rolled)
            else:
                if pts > 0:
                    score += pts
                    num_dice -= remaining
                else:
                    print(f"{self.playerName}'s turn ended with {score} points")
                    return 0
        self.score += score
        return score


if __name__ == "__main__":
    p1 = Player()
    print(next(p1))
