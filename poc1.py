__author__ = 'Chris'

import deadzealand
import re

# extract info from packages
# start_packages = {
#     "None": "vanilla character",
#     "Melee": "(20xp,S:3,E:3,Melee:A,Stealth:N,1:[p:Ninja;p:Silent_Runner;p:Toughness])"
# }


# compile some regular experssions for determining perk requirements
# skill requirement having either A, N, E after a colon
skill_regex = re.compile(r"(\w+\x3a[ANE])")

# Trait, having SPECIAL then colon
trait_regex = re.compile(r"([SPECIAL]\x3a\d+)")

# Perk, starting with small 'p' then colon
perk_regex = re.compile(r"(p\x3a\w+)")

xp_regex = re.compile(r"(\d+xp)")
choice_regex = re.compile(r"(\d\x5b)")

# Race, starting with small 'r' then colon
# race_regex = re.compile(r"(r\x3a\w+)")

# brackets in perk, meaning there is a requirement
# brackets_regex = re.compile(r"(\x28.+\x29)")

# remove perenthesis from description
the_package = deadzealand.start_packages["Melee"]
the_package = re.sub('[()]','',the_package)
parts = the_package.split(',')

print(parts)
for item in parts:
    xp = xp_regex.search(item)
    perks = perk_regex.search(item)
    traits = trait_regex.search(item)
    skills = skill_regex.search(item)
    choice = choice_regex.search(item)
    if xp is not None:
        print('Costs {0}xp'.format(xp.groups()[0][:2]))
    elif perks is not None:
        print('Aquire Perk {0}'.format(perks.groups()[0][2:]))
    elif traits is not None:
        print('Add Trait {0} +{1}'.format(deadzealand.special_traits[traits.groups()[0][:1]], traits.groups()[0][2:]))
    elif choice is not None:
        print('Choice Required: {0}'.format(traits.groups()[0]))



