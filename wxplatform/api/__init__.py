# -*- coding:utf-8 -*-
__author__ = 'alexday'

from flask import Blueprint

api = Blueprint('api', __name__)

from . import weixin
