__author__ = 'Chris'

from app import app
from flask import render_template
from wtforms import IntegerField, StringField, BooleanField, validators
from flask_wtf import Form

import deadzealand


class CharacterSheet(Form):
    character_name = StringField('Character Name',
                                 [validators.Length(min=1, max=60), validators.InputRequired()])
    strength = IntegerField('Strength',default=3,
                            validators=[validators.NumberRange(min=0, max=12)])
    perception = IntegerField('Perception', default=3, validators=[validators.NumberRange(min=0, max=12)])
    endurance = IntegerField('Endurance', default=3, validators=[validators.NumberRange(min=0, max=12)])
    charisma = IntegerField('Charisma', default=3, validators=[validators.NumberRange(min=0, max=12)])
    intelligence = IntegerField('Intelligence', default=3, validators=[validators.NumberRange(min=0, max=12)])
    agility = IntegerField('Agility', default=3, validators=[validators.NumberRange(min=0, max=12)])
    luck = IntegerField('Luck', default=3, validators=[validators.NumberRange(min=0, max=12)])

    # package =

    accept_rules = BooleanField('I accept the site rules',
                                [validators.InputRequired()])


@app.route('/')
@app.route('/index')
def index():
    traits = {}
    traits['perk_list'] = []
    # perk_list = []
    for key, value in deadzealand.perks.items():
        traits['perk_list'].append(deadzealand.Perk(key, value))

    traits['perk_list'].sort(key=lambda perk: perk.name)

    # print(perk_list)

    # return render_template('base.html')
    sheet = CharacterSheet()
    return render_template('base.html', traits=traits, sheet=sheet)
