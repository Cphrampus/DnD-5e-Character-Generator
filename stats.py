import numpy.random
import yaml

# Important stats per class
class_stat = yaml.load(open("Data/class_stat.yaml"))


# try and determine a class based on already assigned ability scores (colville method)
def get_class(character):
    # make array of the class options
    classes = list(class_stat)

    stats = dict(character["stats"])

    # "rank" of the items, i.e., 1st highest, 2nd highest, etc. allowing for ties
    count = 1

    # see if new value is the same as last, i.e., if there is a tie on that level
    val = 0

    # info/debug log
    print(stats)

    # iterate over the scores in order and rank them, so we can determine which class fits best
    for key, value in [(k, stats[k]) for k in sorted(stats, key=stats.get, reverse=True)]:
        # debug log
        print("({}, {}), {}".format(key, value, val))

        # see if there was a tie with the previous score
        if value == val:
            stats[key] = count - 1
        else:
            stats[key] = count
            count += 1
        val = value

    # debug log what the ranks are
    print(stats)

    choices = {}
    while classes:

        # reset score
        score = 0

        # choose a random class to start, not necessary though
        cl = numpy.random.choice(classes)
        classes.remove(cl)

        # Get primary and secondary desirable attributes for the class
        cl_stats = [stat for stat, rank in class_stat[cl].items() if rank == 1]
        cl_stats2 = [stat for stat, rank in class_stat[cl].items() if rank == 2]

        # get the first and second highest stats
        stat = [stat for stat, rank in stats.items() if rank == 1 or rank == 2]

        # debug print class we are evaluation, and what is important to them
        print("{}, primary: {}, secondary: {}".format(cl, cl_stats, cl_stats2))

        # TODO tweak actual weights and score threshold
        # actual scoring
        for s in stat:
            # give points if the stat is a primary/secondary stat, with preference to it being the highest
            if s in cl_stats:
                score += 4 if stats[s] == 1 else 2
            elif s in cl_stats2:
                score += 3 if stats[s] == 1 else 1

            # see if the class is "viable"
            if score > 3:
                choices.update({cl: score})

    # debug print what classes were chosen to choose from
    print(choices)

    # filter down choices if there were any, otherwise assign a random class
    if choices:
        # get the choice,score pairs in descending order based on score
        choices = [(k, choices[k]) for k in sorted(choices, key=choices.get, reverse=True)]

        # filter choices down to the highest scoring ones
        choices = [choice[0] for choice in choices
                   # see if the score is the same as the highest
                   if choice[1] == choices[0][1]]

        print(choices)

        # choose from the highest scored class options
        choice = numpy.random.choice(choices)
    else:
        choice = cl
    return choice


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
