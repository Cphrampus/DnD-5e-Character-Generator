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