__author__ = 'Chris'

import re

special_traits = {'S': 'Strength',
                  'P': 'Perception',
                  'E': 'Endurance',
                  'C': 'Charisma',
                  'I': 'Intelligence',
                  'A': 'Agility',
                  'L': 'Luck',
                  }

skill_ranks = {'N': 'Novice',
               'A': 'Adept',
               'E': 'Expert',
               }

# stats = {'S': 3, 'P': 3, 'E': 3, 'C': 3, 'I': 3, 'A': 3, 'L': 3}

perks = {
    'Sneak_Attack': 'Player may whisper critical to an unaware target once per encounter.',
    'Action_Boy/Girl(A:5)': 'Extra Critical Hit',
    'Adamantine_Skeleton(E:7)': '+1 DR Once per Watch.',
    'Cannibal': 'Allows you to use treat remains as a meal for the purposes for recovering DR',
    'Chem_Resistance(S:5, E:5)': 'Half as likely to get addicted to chems',
    'Chem_Junkie(p:Chem_Resistance)': 'May consume one additional dose of a given drug per watch.',
    'Comprehension(I:7)': 'Increases the discount when turning in skill books',
    'Computer_Whizz(I:4, Science:A)': 'Gives an additional attempt when trying to hack a locked down '
                                      'computer terminal.',
    }

start_packages = {
    "None": "vanilla character",
    "Melee": "(20xp,S:3,E:3,Melee:A,Stealth:N,1[p:Ninja;p:Silent_Runner;p:Toughness])"
}

class Perk:
    # compile some regular experssions for determining perk requirements
    # skill requirement having either A, N, E after a colon
    __skill_regex = re.compile(r"(\w+\x3a[ANE])")

    # Trait, having SPECIAL then colon
    __trait_regex = re.compile(r"([SPECIAL]\x3a\d+)")

    # Perk, starting with small 'p' then colon
    __perk_regex = re.compile(r"(p\x3a\w+)")

    # Race, starting with small 'r' then colon
    __race_regex = re.compile(r"(r\x3a\w+)")

    # brackets in perk, meaning there is a requirement
    __brackets_regex = re.compile(r"(\x28.+\x29)")

    def __init__(self, name, description):
        self.original_name = name
        self.has_prerequisite = False
        self.p_traits = {}
        self.p_skills = {}
        self.p_perks = []
        self.p_race = []

        if name.count('(') > 0:
            self.name = name[:name.index('(')].replace('_', ' ')  # cut out requirement from first bracket
            self.has_prerequisite = True
        else:
            self.name = name.replace('_', ' ')
            self.has_prerequisite = False

        self.description = description
        if self.has_prerequisite:
            self.prerequisite_string = name[name.find("(") + 1:name.find(")")]
            # process prerequisites
            self.__process_prereq()

        else:
            self.prerequisite_string = ""

        return

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__,
                               self.original_name)

    def __str__(self):
        return self.name

    def __process_prereq(self):
        req_perks = self.__perk_regex.findall(self.prerequisite_string)
        req_skills = self.__skill_regex.findall(self.prerequisite_string)
        req_traits = self.__trait_regex.findall(self.prerequisite_string)

        # print(" Requirements:")

        if len(req_skills) > 0:
            # Found a skill
            for i in req_skills:
                self.p_skills[i[:-2].replace('_', ' ')] = skill_ranks[i[-1]]
                # self.p_skills.append({i[:-2].replace('_', ' '): skill_ranks[i[-1]]})
                # print("   {0}: {1}".format(i[:-2].replace('_', ' '), skill_ranks[i[-1]]))

        if len(req_perks) > 0:
            # Found a perk
            for i in req_perks:
                self.p_perks.append(i[2:].replace('_', ' '))
                # print('   {}'.format(i[2:].replace('_', ' ')))

        if len(req_traits) > 0:
            # Found a trait
            for i in req_traits:
                self.p_traits[special_traits[i[0]]] = i[2]
                # print("   {0}: {1}".format(special_traits[i[0]], i[2]))

        return
#
# perk_list = []
# for key, value in perks.items():
#     perk_list.append(Perk(key, value))
#
# perk_list.sort(key=lambda perk: perk.name)
#
# print(perk_list)