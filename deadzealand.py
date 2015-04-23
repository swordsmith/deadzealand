__author__ = 'Chris'

import re


symbols = {'+': 'Add',
           '-': 'Costs',
           '~': 'Requires'}

special_traits = {'S': 'Strength',
                  'P': 'Perception',
                  'E': 'Endurance',
                  'C': 'Charisma',
                  'I': 'Intelligence',
                  'A': 'Agility',
                  'L': 'Luck',
                  }

skill_ranks = {'-': 'Unskilled',
               'N': 'Novice',
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
    "!None!": "",
    "Melee Combat": "(-xp:20,+S:3,+E:3,+Melee:A,+Stealth:N,[+p:Ninja;+p:Silent_Runner;+p:Toughness])",
    "Ranged Combat": "(-xp:20,+P:3,+A:3,+Guns:A,+Explosives:N,[+p:Sniper;+p:Junk_Rounds;+p:Splash_Back])",
    "Doctor/Scientist": "(-xp:20,+L:3,+I:3,[+Medi_cine:A;+Science:A;+Medicine:N,+Science:N],+Energy_Weapons:N,[+p:Educated;+p:Computer_Whizz;+p:Comprehension])",
}


class Stat:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class StartingPackage:
    # Compile regex
    __xp_regex = re.compile(r"^([\x2b\x2d~])(xp):(\d+)$")
    __trait_regex = re.compile(r"^([\x2b\x2d~])([SPECIAL]):(\d+)$")
    __perk_regex = re.compile(r"^([\x2b\x2d~])(p):(\w+)$")
    __skill_regex = re.compile(r"^([\x2b\x2d~])(\w+):([ANE])$")
    __choice_group_regex = re.compile(r"\x5b([\w\x2c\x3a\x2b\x3b]+)\x5d")

    def __init__(self, name, data):
        self.name = name
        self.data = data

        self.xp = 0
        self.traits = {}
        self.skills = {}
        self.perks = []
        self.choices = {}

        self.__parse_data()
        # traits =

    def __parse_data(self):
        raw = re.sub('[()]', '', self.data)
        # extract choices as to not interfeer with other operations as some have commas ","
        print(raw)
        choices = self.__choice_group_regex.findall(raw)
        if choices is not None:

            # print(choices)
            print('choices: {0}'.format(choices))
        parts = []
        # parts = raw.split(',')

        print(self.name)

        for item in parts:
            # print(item)
            xp = self.__xp_regex.search(item)
            trait = self.__trait_regex.search(item)
            perk = self.__perk_regex.search(item)
            skill = self.__skill_regex.search(item)

            if xp is not None:
                print(xp.groups())
                self.xp = xp.groups()[2]

            elif trait is not None:
                print(trait.groups())

            elif perk is not None:
                print(perk.groups())

            elif skill is not None:
                print(skill.groups())

            else:
                print(item)


    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__,
                               self.name,
                               self.data)

    def __str__(self):
        return self.name


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
# perk_list.append(Perk(key, value))
#
# perk_list.sort(key=lambda perk: perk.name)
#
# print(perk_list)

package_list = []
for key, value in start_packages.items():
    package_list.append(StartingPackage(key, value))

# package_list.append(StartingPackage('Doctor/Scientist', start_packages['Doctor/Scientist']))
package_list.sort(key=lambda package: package.name)
print(package_list)