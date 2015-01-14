# -*- coding:utf-8 -*-
__author__ = 'alexday'

from backend.app import *

backendApp = app

# 以Flask原生服务模式运行
if __name__ == '__main__':
    backendApp.run(host=None, port=9000, debug=True)
