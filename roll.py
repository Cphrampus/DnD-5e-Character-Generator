from heapq import nlargest
from numpy import std
import numpy.random


# roll 4 6-sided dice and keep the highest three
def roll_stat():
    return sum(nlargest(3, numpy.random.random_integers(1, 6, 4)))


# use the roll_stat method to return 6 stats
def roll_stats():
    return [stat for stat in [roll_stat() for _ in range(6)]]


# returns the modifier given a score, ranges from -5 for 1 and +5 for 20
def get_mod(score):
    return (score - 10) // 2

# roll stats and make sure the the sum of the mods is at least 5, the sum of the standard array
def roll_stats_min_mod():
    stats = roll_stats()
    while sum([get_mod(i) for i in stats]) < 5:
        stats = roll_stats()
    return sorted(stats, reverse=True)
