__author__ = 'Chris'

from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.secret_key = 'Better change this 1234'

    return app


app = create_app()

from app import views