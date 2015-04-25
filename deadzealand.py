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

skills = {
    'Barter': [
        ['Novice 5% bonus to buying/selling items.'],
        ['Adept(C:3) 10% bonus to buying/selling items.'],
        ['Expert(C:6) 15% bonus to buying/selling. Requires at least 1 minute of rp.'], ],
    'Energy Weapons': [
        ['Novice may use stun grenade (disable robotics, stun organics)'],
        ['Adept (P:3) may use large energy weapons'],
        ['Expert (P:6) may use any automatic energy weapon'], ],
    'Guns': [
        ['Novice may use pistols'],
        ['Adept (A:3) may use any large firearm'],
        ['Expert (A:6) may use any automatic firearms'], ],
    'Explosives': [
        ['Novice may use up to 3 grenades per day'],
        ['Adept (I:3) may set 3 traps per day'],
        ['Expert (I:6) may throw an extra 3 grenades and set and extra 3 traps'], ],
    'Lock pick': [
        ['Novice-Expert allows you to unlock the corresponding locks'],
        ['Adept (A:3)'],
        ['Expert (A:6)'], ],
    'Medicine': [
        ['Novice allows you to apply bandages or splits to crippled limbs/torso, may stabalise a dying character'],
        ['Adept (I:3) may perform surgery to return one Damage Resistance per watch and may use medicine',
         'to cure poison or sickened effects'],
        ['Expert (I:6) may resuscitate a character who has been dead for up to 5 minutes.'], ],
    'Melee weapons': [
        ['Novice may use short weapons (knives, night sticks etc.)'],
        ['Adept (S:3) may use long melee weapons (swords, axe etc.)'],
        ['Expert (S:6) may use 2-handed weapons (spear or similar)'], ],
    'Repair': [
        ['Novice may jury rig using duct tape and one in five bullets are usable'],
        ['Adept (P:3) may repair damaged weapons using a tool kit and two in five bullets ',
         'recovered are usable'],
        ['Expert (P:6) may repair broken items using just duct tape and three in five bullets are usable.'], ],
    'Science': [
        ['Novice attempt to hack terminals'],
        ['Adept (I:3) may craft medical supplies'],
        ['Expert (I:6) allows you to create chems'], ],
    'Stealth': [
        ['Requires nearby cover or crowd Novice allows 1 minute of stealth'],
        ['Adept (A:3) allows 2 minutes of stealth and may pick-pocket a single item from a targeted ',
         'individual while stealthed'],
        ['Expert (A:6) allows 3 minutes and you may also pick-pocket all items from a targeted container ',
         'while stealthed. '], ],
    'Speechcraft': [
        ['Novice 5% bonus to buying/selling services'],
        ['Adept (C:3) 10% bonus to buying/selling services'],
        ['Expert (C:6) 15% bonus to buying/selling services.'], ],
    'Survival': [
        ['Novice may recover junk from scavenging and 10 bullets total'],
        ['Adept (P:3) may recover plant samples and 15 bullets total'],
        ['Expert (P:6) may recover creature organs and 20 bullets total.'], ],

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
    'Computer_Whizz(I:4,Science:A)': 'Gives an additional attempt when trying to hack a locked down '
                                     'computer terminal.',
    'Demolition_Expert(P:5,A:4,Explosives:A)': 'Gives an extra 2m diameter on traps',
    'Educated(I:4)': 'Have the equivalent of a high school education or higher(basic math,reading and writing)',
    'Explorer(P:7,Survival:N)': 'Gain extra downtime action',
    'Fast metabolism(E:7)': 'restore an extra DR when using stim packs',
    'Fortune Finder(L:7)': 'Gain extra 50 caps once per downtime phase on positive downtime actions.',
    'Ghastly Scavenger(p:Cannibal)': 'May eat the remains of any creature to gain DR.',
    'Hand Loader(P:4,Repair:N,Survival:N)': 'can recover extra usable ammo',
    'Hit the Deck(A:5,P:4)': 'Can call resist against one grenade. This should be roll played by hitting the ground.',
    'Hunter(Survival:E)': ' Gain one extra creature reagent during downtime',
    'Infiltrator(A:5,Lock_Picking:A)': 'Can pick locks while stealthed',
    'Jury-Rigger(Repair:A)': ' Jury rigging lasts twice as long',
    'Lead Belly(E:8)': 'Ignores radiation from food or water sources',
    'Life Giver': '+1 DR',
    'Light Step(P:8)': 'May resist one trap effect. Trap does not activate',
    'Living Anatomy(Medicine:A,I:6)': 'When using adept medicine,can grant one additional DR per use. Also grants an additional draw from fate bag when using resuscitation ability of Medicine expert.',
    'Math Wrath(I:6,p:Educated)': 'Grants 5% bonus to barter',
    'Merchant(Charisma:5,Barter:A)': 'Begin each weekend game with 60 caps',
    'Nerves of Steel(I:4,C:4)': 'Regain one extra critical per watch',
    'Night Person(P:5)': ' During any of the night watches,Bonus spot/clue',
    'Solar Powered(P:5)': 'During daytime watches,bonus spot/clue',
    'Ninja(A:6,Stealth:N)': 'Melee critical do not break stealth',
    'Nuka-Chemist(I:10)': 'Can convert Nuka-cola to one of the nuka-cola special edition types',
    'Pack Rat(Barter:A)': 'May carry 2 extra loot sheets',
    'Paralysing Arm(S:10,A:6)': 'May stun using a touch attack',
    'Pyro-maniac(P:8,E:4)': 'Can use fire weapons',
    'Rad Absorption(E:10)': 'Rad level reduced by one per watch',
    'Rad Resistance(E:12)': 'Ignore the first level of radiation sickness once per day.',
    'Robotics(I:10,Science:E)': 'May touch attack unaware robots to deactivate them.',
    'Scrounger(P:5,Survival:A)': 'Gain additional ammo during downtime',
    'Silent Runner(A:5,P:4)': 'May run while using stealth',
    'Sniper(A:7,Guns:A)': 'Extra gun crit.',
    'Splash Back(Explosives:E)': 'Grenades have 2m greater diameter',
    'Stonewall(E:10)': 'May resist knockback',
    'Strong Back(S:9)': 'Can carry and extra 2 loot sheets',
    'Strong-wall(S:10)': 'Can call knock back on a melee strike',
    'Professional *Phys rep*(I:6,A:8,Guns:E)': 'May attach silencers to firearms,allowing ranged critical while stealthed.',
    'Toughness': '+1 DR',
    'Recycler(I:5)': 'allows you to recover energy weapon ammo.',
    'Weapon handling *must specify weapon type*': 'May call an additional critical with a weapon of the player’s choice.',
    'And Stay Back(A:10)': ' Can call knockback with ranged weapons',
    'In shining armour(E:12,Phys Rep)': 'May call resist(using DR) against laser weapons when wearing shining/metal armour',
    'Junk rounds(Repair:A)': 'Can construct bullets out of junk',
    'Epicurean': 'You are less prone to chem addiction. May consider a bottle of alcohol a meal for the purposes of E:recovery. ',
    'Alertness(P:8)': 'Additional spot once per watch',
    'Certified Tech(I:7,Science:E)': 'May recover crafting components from robots',
    'Irradiated Beauty *Ghoul Specific*': 'sleep removes one rad level',
    'Thought you Died *requires GM discussion*': 'Resets all reputation to Neutral.',
    'Walker Instinct(P:6)': 'Once per watch,extra spot while outside',
    'Mad Bomber(I:7,Explosives:E)': 'Allows you to create fire,EMP or poison bombs',

}

start_packages = {
    "-": "",
    "Melee Combat": "(-xp:20,+S:3,+E:3,+Melee:A,+Stealth:N,[+p:Ninja;+p:Silent_Runner;+p:Toughness])",
    "Ranged Combat": "(-xp:20,+P:3,+A:3,+Guns:A,+Explosives:N,[+p:Sniper;+p:Junk_Rounds;+p:Splash_Back])",
    "Doctor/Scientist": '(-xp:20,+L:3,+I:3,[+Medicine:A;+Science:A;+Medicine:N,+Science:N],+Energy_Weapons:N,'
                        '[+p:Educated;+p:Computer_Whizz;+p:Comprehension])',
    "Scavenger": '(-xp:20,+C:3,+I:3,+Survival:N,[+Guns:N;+Melee:N],[+Repair:N;+Barter:N],[+p:Hunter;+p:Explorer;+p:Fortune_Finder])'
}

regex_perk_name = re.compile(r'^([\w ]+)')


class Stat:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Skill:
    def __init__(self, name, data):
        self.name = name
        self.value = 0
        self.data = data
        self.novice_data = self.data[0]
        self.adept_data = self.data[1]
        self.expert_data = self.data[2]


class StartingPackage:
    # Compile regex
    __xp_regex = re.compile(r"^([\x2b\x2d~])(xp):(\d+)$")
    __stat_regex = re.compile(r"^([\x2b\x2d~])([SPECIAL]):(\d+)$")
    __perk_regex = re.compile(r"^([\x2b\x2d~])(p):(\w+)$")
    __skill_regex = re.compile(r"^([\x2b\x2d~])(\w+):([ANE])$")
    __choice_group_regex = re.compile(r"(,?\x5b[\w\x2c\x3a\x2b\x3b]+\x5d)")
    # __choice_group_regex = re.compile(r"\x5b([\w\x2c\x3a\x2b\x3b]+)\x5d")

    def __init__(self, name, data):
        self.name = name
        self.data = data

        self.xp = 0
        self.stats = {}
        self.skills = {}
        self.perks = []
        self.choices = {}

        self.__parse_data()
        # traits =

    def __parse_data(self):
        # print('\n', self.name)
        raw = re.sub('[()]', '', self.data)
        # extract choices as to not interfere with other operations as some have commas ","
        # print(raw) if raw else None
        choices = self.__choice_group_regex.findall(raw)
        raw = self.__choice_group_regex.sub('', raw)
        options = []

        # choices = []
        if choices:
            # print('choices: {0}'.format(choices))
            for i in choices:
                choice = []
                # remove the square brackets
                cleaned_choice = re.sub('[\x5d\x5b]', '', i[1:])
                # print(cleaned_choice)
                # a ";" means OR as in +Medicine:A;+Science:A is Medicine OR Science
                # a "," is AND
                items = cleaned_choice.split(';')
                # print('options: ', items, '\n')
                options.append(items)
        # print(options)

        parts = []
        # parts = raw.split(',')


        for item in parts:
            # print(item)
            xp = self.__xp_regex.search(item)
            # print(xp)
            stat = self.__stat_regex.search(item)
            perk = self.__perk_regex.search(item)
            skill = self.__skill_regex.search(item)

            if xp is not None:
                print("xp groups 111: ", xp.groups())
                self.xp = xp.groups()[2]

            elif stat is not None:
                print(stat.groups())

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


def parse_trait(data):
    # Compile regex
    xp_regex = re.compile(r"^([\x2b\x2d~])(xp):(\d+)$")
    stat_regex = re.compile(r"^([\x2b\x2d~])([SPECIAL]):(\d+)$")
    perk_regex = re.compile(r"^([\x2b\x2d~])(p):(\w+)$")
    skill_regex = re.compile(r"^([\x2b\x2d~])(\w+):([ANE])$")
    choice_group_regex = re.compile(r"(,?\x5b[\w\x2c\x3a\x2b\x3b]+\x5d)")
    trait = None

    skill = skill_regex.match(data)
    if skill is not None:
        trait = {skill.groups()[1]: skill.groups()[2]}
        # trait = {skill.groups()[1]: skill.groups()[2]}
    perk = perk_regex.match(data)
    if perk is not None:
        # trait = perk.groups()[2]
        trait = perk_list[perk.groups()[2]]
    stat = stat_regex.match(data)
    if stat is not None:
        trait = {special_traits[stat.groups()[1]]: stat.groups()[2]}

    return trait


#
perk_list = {}
for key, value in perks.items():
    tmp = regex_perk_name.match(key)
    clean_key = tmp.groups()[0] if tmp is not None else key
    perk_list[clean_key] = (Perk(key, value))

skill_list = {}
for key, value in skills.items():
    skill_list[key] = Skill(key, value)
#
# perk_list.sort(key=lambda perk: perk.name)
#
# print(perk_list)

# package_list = []

package_list = {}
for key, value in start_packages.items():
    package_list[key] = StartingPackage(key, value)

    # package_list.append(StartingPackage(key, value))

# package_list.append(StartingPackage('Doctor/Scientist', start_packages['Doctor/Scientist']))
# package_list.sort(key=lambda package: package.name)
# print(package_list)

# '(-xp:20,+C:3,+I:3,+Survival:N,[+Guns:N;+Melee:N],[+Repair:N;+Barter:N],[+p:Hunter;+p:Explorer;+p:Fortune_Finder])'
print('---')
# print(parse_trait('+Survival:N'))
# print(parse_trait('+C:3'))
# print(parse_trait('+p:Hunter'))
