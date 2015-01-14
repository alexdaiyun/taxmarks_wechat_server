# -*- coding:utf-8 -*-
__author__ = 'alexday'

from bae.core.wsgi import WSGIApplication

from backend.app import *

backendApp = app

# 支持百度BAE
# 将stderr输出到标准出错的日志，重定向到BAE日志服务器
application = WSGIApplication(backendApp, stderr='log')
