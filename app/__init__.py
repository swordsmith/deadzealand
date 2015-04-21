__author__ = 'Chris'

from flask import Flask

def create_app():
    app = Flask(__name__)
    # Bootstrap(app)

    return app


app = create_app()

from app import views