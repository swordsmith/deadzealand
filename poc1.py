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
skill_regex = re.compile(r"^([\x2b\x2d~])(\w+):([ANE])$")

# Trait, having SPECIAL then colon
trait_regex = re.compile(r"([SPECIAL]\x3a\d+)")

# Perk, starting with small 'p' then colon
perk_regex = re.compile(r"^([\x2b\x2d~])(p\x3a\w+)")
perk2_regex = re.compile(r"^([\x2b\x2d~])(p):(\w+)$")

xp_regex = re.compile(r"([\x2b\x2d~])(\d+xp)")
# choice_regex = re.compile(r"(\d\x5b)")
choice_regex = re.compile(r"(\d+)\x5b(.+)\x5d")

# Race, starting with small 'r' then colon
# race_regex = re.compile(r"(r\x3a\w+)")

# brackets in perk, meaning there is a requirement
# brackets_regex = re.compile(r"(\x28.+\x29)")

# remove perenthesis from description
the_package = deadzealand.start_packages["Melee"]
the_package = re.sub('[()]','',the_package)
parts = the_package.split(',')
symbols = {'+': 'Add',
           '-': 'Costs',
           '~': 'Needs'}

print(parts)
for item in parts:
    xp = xp_regex.search(item)
    perks = perk_regex.search(item)
    traits = trait_regex.search(item)
    skills = skill_regex.search(item)
    choice = choice_regex.search(item)

    if xp is not None:
        print('{0} {1}'.format(symbols[xp.groups()[0]], xp.groups()[1]))

    if skills is not None:
        print('{0} Skill {1}:{2}'.format(symbols[skills.groups()[0]], skills.groups()[1], deadzealand.skill_ranks[skills.groups()[2]]))

    elif perks is not None:
        print('{0} Perk {1}'.format(symbols[perks.groups()[0]], perks.groups()[1][2:]))

    elif traits is not None:
        print('Add Trait {0} +{1}'.format(deadzealand.special_traits[traits.groups()[0][:1]], traits.groups()[0][2:]))

    elif choice is not None:
        print('Choice Required: {0}'.format(choice.groups()[0]))
        choose_list = choice.groups()[1].split(';')
        print(choose_list)

        for j in choose_list:
            choice_perk = perk2_regex.search(j)
            choice_skill = skill_regex.search(j)

            # print(choice_perk.groups())
            # print(choice_skill.groups())

            if choice_perk is not None:
                print(choice_perk.groups())
                # pass

            if choice_skill is not None:
                pass





