__author__ = 'Chris'

from app import app
from flask import render_template, jsonify, request, sessions
from wtforms import IntegerField, StringField, BooleanField, SelectField ,validators
from flask_wtf import Form
import jsonpickle

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

    package = SelectField('Package', choices=deadzealand.package_list.keys())

    accept_rules = BooleanField('I accept the site rules',
                                [validators.InputRequired()])


@app.route('/')
@app.route('/index')
def index():
    traits = {}
    traits['perk_list'] = []
    lists = {}
    # perk_list = []
    for key, value in deadzealand.perks.items():
        traits['perk_list'].append(deadzealand.Perk(key, value))

    traits['perk_list'].sort(key=lambda perk: perk.name)
    lists['packages'] = list(deadzealand.start_packages.keys())
    # lists['skills'] = list(deadzealand.start_packages.keys())
    lists['packages'].sort()

    # print(perk_list)

    # return render_template('base.html')
    sheet = CharacterSheet()
    return render_template('base.html', traits=traits, sheet=sheet, lists=lists)

@app.route('/_get_package')
def get_package_stats():
    the_package = request.args.get('the_package', 'none found', type=str)
    package_data = deadzealand.package_list[the_package]
    data = jsonpickle.encode( package_data, unpicklable=False, max_depth=10)

    # print(data)

    package_html = render_template('package-select-result.html', traits=package_data)
    # return jsonify( details=package_html )
    return jsonify(package_html=package_html, package=data)
