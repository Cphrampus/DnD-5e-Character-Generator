import os

import yaml



# import yaml file for race weights
races = yaml.load(open("Data/races.yaml", "r"))


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
