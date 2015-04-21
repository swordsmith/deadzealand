__author__ = 'Chris'

from app import app
from flask import render_template

import deadzealand


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
    return render_template('base.html', traits=traits)
