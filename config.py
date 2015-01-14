# -*- coding:utf-8 -*-
__author__ = 'alexday'

import os
import logging
from hashlib import md5

basedir = os.path.abspath(os.path.dirname(__file__))

"""
正式环境

APP_CONFIG = {
    'MP_SERVER_HOST': u'http://taxmarksmp.duapp.com',  # MP_SERVER的主机地址
    'SSO_SERVER_HOST': u'http://www.taxmarks.com:8100',  # 提供SSO服务的地址
    'TAXMARKS_WEIXINWEB_HOST': u'http://www.taxmarks.com/taxmarkswxweb',  # taxmarks weixinweb的主机地址
    'WE_CENTER_HOST': u'http://218.244.132.167:8080'  # WeCenter的主机地址
}

MP_CCONFIG = {
    'MP_TOKEN_KEY': u'rismotax1234',
    'MP_AppID': u'wx37d853e02c8a692c',
    'MP_AppSecret': u'5b20fcb9c6b42b76a5c44b093ed46ecb'
}

BAE_ApiKey = 'ZwzUxUgBv7p27a55lf50K11F'
BAE_SecretKey = 'XuNLVZW3DPdzVbiy69twLVmYgPPNO7Ga'


测试环境


APP_CONFIG = {
    'MP_SERVER_HOST': u'http://helixappserver3.duapp.com',  # MP_SERVER的主机地址
    'SSO_SERVER_HOST': u'http://218.244.132.167:8091',  # 提供SSO服务的地址
    'TAXMARKS_WEIXINWEB_HOST': u'http://218.244.132.167:8090',  # taxmarks weixinweb的主机地址
    'WE_CENTER_HOST': u'http://218.244.132.167:8080'  # WeCenter的主机地址
}

MP_CCONFIG = {
    'MP_TOKEN_KEY': u'abcd1234',
    'MP_AppID': u'wx3ef755a9cf4666ef',
    'MP_AppSecret': u'4042e8bafb7c49f812b3e06b5708d841'
}

BAE_ApiKey = 'T691k52Yf8qgGDFBPaggCEhA'
BAE_SecretKey = 'lSd8cyfEPCTBTp3MjIetgUg9YVem8UWO'


"""


class Config:
    # tip: generate `SECRET_KEY` by `os.urandom(24)`
    # use os.urandom(24) to generate a key.
    # os.getenv('SECRET_KEY') or 'hard to guess string'
    def __init__(self):
        pass

    APP_SECRET_KEY = u'\xf8\xac\xf8(a\xa7\xf6\xab\xf0\xaf>\x0e\x9e\xf6\xa5\xb9\xc4\x87\xbeR\xdc\x87/\xf3'

    APP_CONFIG = {
        'MP_SERVER_HOST': u'http://taxmarksmp.duapp.com',  # MP_SERVER的主机地址
        'SSO_SERVER_HOST': u'http://www.taxmarks.com:8100',  # 提供SSO服务的地址
        'TAXMARKS_WEIXINWEB_HOST': u'http://www.taxmarks.com/taxmarkswxweb',  # taxmarks weixinweb的主机地址
        'WE_CENTER_HOST': u'http://218.244.132.167:8080'  # WeCenter的主机地址
    }

    # MP - weChat
    # Token Key and AppID and AppSecret
    MP_CONFIG = {
        'MP_TOKEN_KEY': u'rismotax1234',
        'MP_AppID': u'wx37d853e02c8a692c',
        'MP_AppSecret': u'5b20fcb9c6b42b76a5c44b093ed46ecb'
    }

    @staticmethod
    def get_mailhandler():
        mail_handler = {}
        return mail_handler

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data_dev_sqlite.db')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data_sqlite.db')

    # mysql configuration
    MYSQL_USER = os.getenv('MYSQL_USER') or ''
    MYSQL_PASS = os.getenv('MYSQL_PASS') or ''
    MYSQL_HOST = os.getenv('MYSQL_HOST') or ''
    MYSQL_PORT = os.getenv('MYSQL_PORT') or ''
    MYSQL_DB = os.getenv('MYSQL_DB') or ''

    if (len(MYSQL_USER) > 0 and len(MYSQL_PASS) > 0 and
            len(MYSQL_HOST) > 0 and len(MYSQL_PORT) > 0 and
            len(MYSQL_DB) > 0):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or \
            'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST,
                                        MYSQL_PORT, MYSQL_DB)

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class BAEConfig(Config):
    # BAE - Baidu Application Engine
    # API Key and Secret Key
    BAE_AK = os.getenv('BAE_AK') or 'ZwzUxUgBv7p27a55lf50K11F'
    BAE_SK = os.getenv('BAE_SK') or 'XuNLVZW3DPdzVbiy69twLVmYgPPNO7Ga'

    # mysql configuration
    MYSQL_USER = os.getenv('MYSQL_USER') or BAE_AK
    MYSQL_PASS = os.getenv('MYSQL_PASS') or BAE_SK
    MYSQL_HOST = os.getenv('MYSQL_HOST') or 'sqld.duapp.com'
    MYSQL_PORT = os.getenv('MYSQL_PORT') or '4050'
    MYSQL_DB = os.getenv('MYSQL_DB') or ''

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or \
        'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST,
                                    MYSQL_PORT, MYSQL_DB)

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        def _create_logger(bufcount=256):
            _logger = logging.getLogger()
            _logger.setLevel(logging.DEBUG)
            from bae_log import handlers
            _handler = handlers.BaeLogHandler(
                ak=app.config.get('BAE_AK'),
                sk=app.config.get('BAE_SK'),
                bufcount=bufcount
            )
            return _handler
        _logger = _create_logger(1)
        app.logger.addHandler(_logger)


class SAEConfig(Config):

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        _handler = logging.StreamHandler()
        app.logger.addHandler(_handler)


config = {
    'bae': BAEConfig,
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'local': DevelopmentConfig,
    'production': ProductionConfig,
    'sae': SAEConfig,
}