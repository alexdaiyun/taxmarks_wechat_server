# -*- coding:utf-8 -*-
__author__ = 'alexday'

import os

from backend import create_app, get_appconfig

# bae, sae, production, local(default)
app = create_app(os.getenv('APP_CONFIG') or str(get_appconfig()) or 'default')

# if __name__ == '__main__':
#    app.run()