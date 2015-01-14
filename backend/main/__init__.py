# -*- coding:utf-8 -*-
__author__ = 'alexday'

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
