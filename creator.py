import os

import yaml
import numpy.random



# import yaml file for race weights
races = yaml.load(open("Data/races.yaml", "r"))


# given a list of values with weights, randomly pick one
def random_from(items):
    # make a value weight tuple for each item, them zip them so there is a value array and a weight array
    values, weights = zip(*[(value, items[value]["weight"]) for value in items])
    total = sum(weights)
    probs = [weight / total for weight in weights]
    return numpy.random.choice(values, p=probs)


def create():
    # create an array of values to keep track of choices
    attr = []

    # create object to return as created character info
    character = {}

    # choose a random race and add it to the list
    race = random_from(yaml.load(open("Data/races.yaml")))
    attr += [race]

    # choose a random subrace of our chosen race and add it to the list
    subrace = random_from(yaml.load(open("Data/Gen/{}/subraces.yaml".format(*attr))))
    attr += [subrace]

    # choose a random background for our race/subrace choices
    background = random_from(yaml.load(open("Data/Gen/{}/{}/backgrounds.yaml".format(*attr))))

    # save choices to character
    character["background"] = background
    character["race"] = race

    # not all races have subraces
    character["subrace"] = subrace if subrace != "" else None

    cl = random_from(yaml.load(open("Data/Gen/{}/{}/classes.yaml".format(*attr))))

    # save class choice
    attr += [cl]

    # choose random archetype for our choices thus far
    archetype = random_from(yaml.load(open("Data/Gen/{}/{}/{}/archetypes.yaml".format(*attr))))

    # print out our choices
    print(background, race + ("({})".format(subrace) if subrace != "" else ""), cl + "({})".format(archetype))

    # save class and archetype to character
    character["class"] = cl
    character["archetype"] = archetype

    return character


# TODO modify to break down into yamls including stats, mods, etc.
# TODO refactor
# generates basic yaml files, should only be used for creating all files
# does not deal with modifiers, proficiencies, or anything above weighting everything the same
def gen_yamls():
    # base path for Data Gen folder
    basepath = "Data/Gen/"
    os.makedirs(basepath, 0o700, True)

    # make a folder for each race
    for race in sorted(races):
        path = basepath
        os.makedirs(path+race, 0o700, True)
        path += race

        subracePath = path
        # make a list of subraces for each race
        with open(path+"/subraces.yaml", "w") as subraces_file:
            subraces = races[race]["subraces"]
            if subraces is None:
                subraces = [""]
            for subrace in subraces:
                path = subracePath
                subraces_file.write("\"{}\":\n  weight: 2\n".format(subrace))
                if subrace:
                    os.makedirs(path+"/"+subrace, 0o700, True)
                    path += "/"+subrace

                classPath = path
                # make a list of classes for each subrace
                with open(path+"/classes.yaml", "w") as classes:
                    path = classPath
                    cl = yaml.load(open("Data/classes.yaml"))
                    for c in sorted(cl):
                        classes.write("\"{}\":\n  weight: 2\n".format(c))
                        os.makedirs(path+"/"+c, 0o700, True)

                        # make a list of archetypes for the class
                        with open(path+"/"+c+"/archetypes.yaml", "w") as archetypes:
                            for archetype in sorted(cl[c]["archetypes"]):
                                archetypes.write("\"{}\":\n  weight: 2\n".format(archetype))

                # make a list of backgrounds for each subrace
                with open(path + "/backgrounds.yaml", "w") as backgrounds:
                    for background in sorted(yaml.load(open("Data/backgrounds.yaml"))):
                        backgrounds.write("\"{}\":\n  weight: 2\n".format(background))
