# dice-10000
CS 181Y/35 project Harvey Mudd

https://en.wikipedia.org/wiki/Dice_10000

There are many variations but the rules I'm going with for now are:

1. 3 ones is 1000, for 3 of a kind of 2-6 inclusive multiply by 100
2. otherwise 1 is 100 and 5 is 50
3. if you use up all the dice you can roll again and those points are 
adding to a running total

- [X] Front-end
- [X] Flask backend

# Strategies
- [X] Strategy A: Only roll until the score of the turn is up to one number(i.e. 500)
- [X] Strategy B: Only roll if you have a certain number of dice(1-6)
- [X] Strategy AB: Strategy AB: roll if more dice than a number otherwise until target score is reached
- [X] User input player object to connect with front-end
- [ ] Strategy C: Same as A but don't take triples unless you have to or its 500, 600, or 1000
- [ ] Strategy D: Same as B but don't take triple unless you have to or its 500, 600, or 1000
- [ ] Last round/endgame strategy/rules

# Additional rules(the game's rules and names vary a lot)
- [ ] On the 1st turn you must roll until you reach 500 "to get on the board"
- [ ] If four, five, or six of a kind are rolled, each additional dice is worth as much again as the three of a kind score
    This makes the highest possible score in a single roll 4000 for six ones (1000 for three ones, after that player gains 1000 points for each additional one in that series of rolling) The ONE is the only dice you ever count in the thousands.
- [ ] A straight from 1 to 6 is worth 1500 points. If a player fails to roll a straight they may make one attempt to complete the straight. If the desired number(s) does not turn up on the next roll that round is a "crap out" even if there are scoring dice on the table i.e. 1's or 5's
- [ ] Three pairs are worth 1500 points. For instance 2+2, 4+4, 5+5. This rule does not count if you roll a quadruple and a pair e.g. 2+2, 2+2, 6+6 unless stated otherwise (some places have their own house rules)
- [ ] If a player fails to roll a three pairs, they may make one attempt to complete the three of a kind. If the desired number(s) does not turn up on the next roll, that round is a "crap out", even if there are scoring dice on the table; i.e. 1's or 5's
