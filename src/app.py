# -*- coding: utf-8 -*-

from flask import Flask
from controllers.controller_sunrise_sunset import sunrise_sunset_bp


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(sunrise_sunset_bp)
