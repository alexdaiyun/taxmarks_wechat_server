# -*- coding:utf-8 -*-
__author__ = 'alexday'

from flask import request, jsonify, redirect, render_template, make_response
from . import main

@main.app_errorhandler(400)
def error_bad_request(e):
    return make_response(jsonify({'status': False, 'errormsg': u'参数错误'}), 400)


@main.app_errorhandler(403)
def forbidden(e):
    """Render a custom template when responding with 403."""
    _template = 'errors/403.html'
    return render_template(_template), 403


@main.app_errorhandler(404)
def page_not_found(e):
    """Render a custom template when responding with 404 Not Found."""
    _template = 'errors/404.html'
    return render_template(_template), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """Render a custom template when responding with 505."""
    _template = 'errors/500.html'
    return render_template(_template), 500