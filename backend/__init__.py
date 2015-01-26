# -*- coding:utf-8 -*-
__author__ = 'alexday'

import os
import sys

from flask import Flask

from config import config


def get_appconfig():
    _env = os.getenv('SERVER_SOFTWARE')
    if _env:
        if _env.startswith('bae'):
            env = 'bae'
        elif _env.startswith('direwolf'):
            env = 'sae'
        else:
            env = 'production'
    else:
        env = 'local'
    return env


def create_app(config_name):

    reload(sys)
    sys.setdefaultencoding('utf-8')

    app = Flask(__name__)

    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app