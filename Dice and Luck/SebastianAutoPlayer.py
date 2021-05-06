# Automatic Sebastian game player
# B551 Fall 2020
# Code by bgoginen-surgudla-tsadey
#
# Based on skeleton code by D. Crandall
#
#
# This is the file you should modify to create your new smart player.
# The main program calls this program three times for each turn.
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list
#      of dice indices that should be re-rolled.
#
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

from SebastianState import Scorecard
import random


class SebastianAutoPlayer:

    def __init__(self):
        self.cat_auto = []

    # Returns score for the die combinations for the category passed as a parameter
    def calculate_score(self, dice1, category):
        score = {}
        counts = [dice1.count(i) for i in range(1, 7)]
        if category in Scorecard.Numbers:
            score = counts[Scorecard.Numbers[category] - 1] * Scorecard.Numbers[category]
        elif category == "company":
            score = 40 if sorted(dice1) == [1, 2, 3, 4, 5] or sorted(dice1) == [2, 3, 4, 5, 6] else 0
        elif category == "prattle":
            score = 30 if (len({1, 2, 3, 4} - set(dice1)) == 0 or len({2, 3, 4, 5} - set(dice1)) == 0 or len(
                {3, 4, 5, 6} - set(dice1)) == 0) else 0
        elif category == "squadron":
            score = 25 if (2 in counts) and (3 in counts) else 0
        elif category == "triplex":
            score = sum(dice1) if max(counts) >= 3 else 0
        elif category == "quadrupla":
            score = sum(dice1) if max(counts) >= 4 else 0
        elif category == "quintuplicatam":
            score = 50 if max(counts) == 5 else 0
        elif category == "pandemonium":
            score = sum(dice1)
        return score

    # Returns indices to be rolled for first re-roll
    def first_roll(self, dice, scorecard):
        best_re_roll, category = self.max_layer(dice, scorecard)
        best_re_roll = list(best_re_roll)
        best_re_roll1 = []
        for i in range(0, len(best_re_roll)):
            if best_re_roll[i]:
                best_re_roll1.append(i)
        return best_re_roll1

    # Returns indices to be rolled for second re-roll
    def second_roll(self, dice, scorecard):
        best_re_roll, category = self.max_layer(dice, scorecard)
        best_re_roll = list(best_re_roll)
        best_re_roll1 = []
        for i in range(0, len(best_re_roll)):
            if best_re_roll[i]:
                best_re_roll1.append(i)
        return best_re_roll1

    # Assigns best category for the given die combination and returns it
    def third_roll(self, dice, scorecard):
        dice = list(str(dice))
        dice = [ele for ele in dice if ele != ' ']
        dice = [int(ele) for ele in dice]
        categories = {}
        # Checks for unassigned list of categories
        for category in list(set(Scorecard.Categories) - set(scorecard.scorecard.keys())):
            categories[category] = self.calculate_score(dice, category)
        cat = next(iter(sorted(categories, key=categories.get, reverse=True)))
        self.cat_auto.append(cat)
        return cat

    # Checks for best re-roll indices
    def max_layer(self, roll1, scorecard):
        max_so_far = (0, 0)
        # consider all possible combinations
        for roll_a in (True, False):
            for roll_b in (True, False):
                for roll_c in (True, False):
                    for roll_d in (True, False):
                        for roll_e in (True, False):
                            exp_score, category = self.expectation_of_re_roll(roll1,
                                                                              (roll_a, roll_b, roll_c, roll_d, roll_e),
                                                                              scorecard)
                            if exp_score > max_so_far[1]:
                                max_so_far = (roll_a, roll_b, roll_c, roll_d, roll_e)
        return max_so_far, category

    # Calculates expectation for each die combination
    def expectation_of_re_roll(self, roll, re_roll, scorecard):
        roll1 = list(str(roll))
        roll2 = [ele for ele in roll1 if ele != ' ']
        roll2 = [int(ele) for ele in roll2]
        outcomes = []
        for out_a in ((roll2[0],) if not (re_roll[0]) else range(1, 7)):
            for out_b in ((roll2[1],) if not (re_roll[1]) else range(1, 7)):
                for out_c in ((roll2[2],) if not (re_roll[2]) else range(1, 7)):
                    for out_d in ((roll2[3],) if not (re_roll[3]) else range(1, 7)):
                        for out_e in ((roll2[4],) if not (re_roll[4]) else range(1, 7)):
                            o = (out_a, out_b, out_c, out_d, out_e)
                            outcomes.append(o)
        outcomes1 = []
        value = {}
        # removes duplicate outcomes by sorting the outcomes
        for o in outcomes:
            outcomes1.append(tuple(sorted(o)))
        outcomes2 = list(set(outcomes1))
        for category in list(set(Scorecard.Categories) - set(scorecard.scorecard.keys())):
            for o in outcomes2:
                value[category] = 0
                value[category] += self.calculate_score(o, category)
            value[category] /= len(outcomes2)
        exp = next(iter(sorted(value, key=value.get, reverse=True)))
        return value[exp], exp
