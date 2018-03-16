import numpy.random
import yaml

# Important stats per class
class_stat = yaml.load(open("Data/class_stat.yaml"))


# using the defined "primary" and "secondary" stats for each class,
# assign scores into the stats that make the most sense
def assign_stats(character, stats):
    # add a stats property to the character to store the array after assignments are done
    character["stats"] = {}

    # pull out the primary and secondary stats for the character's class
    rank1 = [stat for stat, rank in class_stat[character["class"]].items() if rank == 1]
    rank2 = [stat for stat, rank in class_stat[character["class"]].items() if rank == 2]
    rank3 = [stat for stat in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
             if stat not in rank1 and stat not in rank2]

    # assign scores to primary and secondary scores

    # alternate between primary and secondary, multiple just means a choice between them
    # so we will randomly choose one
    flag = True
    while rank1 or rank2:
        if flag and rank1:
            choice = numpy.random.choice(rank1)
            rank1.remove(choice)
            flag = False
        elif rank2:
            choice = numpy.random.choice(rank2)
            rank2.remove(choice)
            flag = True
        else:
            flag = True
            continue

        # assign the highest remaining score to the chosen stat
        character["stats"][choice] = stats[0]
        stats = stats[1:]

    # randomly assign the rest
    while rank3:
        choice = numpy.random.choice(rank3)
        rank3.remove(choice)
        character["stats"][choice] = stats[0]
        stats = stats[1:]
