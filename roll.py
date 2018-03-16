from heapq import nlargest
from numpy import std
import numpy.random


# roll 4 6-sided dice and keep the highest three
def roll_stat():
    return sum(nlargest(3, numpy.random.random_integers(1, 6, 4)))


# use the roll_stat method to return 6 stats
def roll_stats():
    return [stat for stat in [roll_stat() for _ in range(6)]]
