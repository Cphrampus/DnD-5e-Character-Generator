import numpy.random
import yaml


# racial modifiers
race_mods = yaml.load(open("Data/race_mods.yaml"))

# background proficiencies
background_profs = yaml.load(open("Data/backgrounds.yaml"))

# racial bonuses
race_bonuses = yaml.load(open("Data/race_bonuses.yaml"))

# class details
class_details = yaml.load(open("Data/class_details.yaml"))


# add stat changes from races
def add_racial_modifiers(character):
    race = character["race"]
    mods = race_mods[race]

    # half elves get Charisma +2, plus +1 to 2 others of their choice
    if character["race"] == "HalfElf":
        # TODO refactor to just grab two at random and update the mods
        choices = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom"]
        for _ in range(2):
            choice = numpy.random.choice(choices)
            mods.update({choice: 1})
            choices.remove(choice)

    to_remove = []

    # add any relevant modifiers for the subrace
    if mods["subrace"]:
        # update any modifiers that exist for the subrace
        mods.update(mods[character["subrace"]])

        # remove any mods that are dictionaries, i.e., subrace elements
        for i, val in mods.items():
            if isinstance(val, dict):
                to_remove.append(i)

        for i in to_remove:
            del mods[i]

    # remove the bool of whether the race has subraces or not
    del mods["subrace"]

    # add modifiers that the character gets
    for mod in mods:
        character["stats"][mod] += mods[mod]
