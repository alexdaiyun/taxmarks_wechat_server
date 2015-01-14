# -*- coding:utf-8 -*-
__author__ = 'alexday'

from wxplatform.index import *

wxplatformServer = app

# 以Flask原生服务模式运行
if __name__ == '__main__':
    wxplatformServer.run(host=None, port=9001, debug=True)
