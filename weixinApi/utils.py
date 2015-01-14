# -*- coding:utf-8 -*-
"""
    weixinApi.utils
    ~~~~~~~~~~~~~~~
    This module provides some useful utilities.

"""
__author__ = 'alexday'


import re
import random
import json
import six
import time
import hashlib


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


class NotNoneDict(dict):
    """A dictionary only store non none values"""

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        if value is None:
            return
        return dict_setitem(self, key, value)


class WeiXinSigner(object):
    """WeiXin data signer"""

    def __init__(self):
        self._data = []

    def add_data(self, *args):
        """Add data to signer"""
        for data in args:
            self._data.append(to_binary(data))

    @property
    def signature(self):
        """Get data signature"""
        self._data.sort()
        str_to_sign = b''.join(self._data)
        return hashlib.sha1(str_to_sign).hexdigest()


def check_signature(token, signature, timestamp, nonce):
    """Check weixin  callback signature, raises InvalidSignatureException
    if check failed.

    :param token: weixin callback token
    :param signature: weixin callback signature sent by weixin server
    :param timestamp: weixin callback timestamp sent by weixin server
    :param nonce: weixin callback nonce sent by weixin sever
    """
    signer = WeiXinSigner()
    signer.add_data(token, timestamp, nonce)
    if signer.signature != signature:
        from .exceptions import InvalidSignatureException

        raise InvalidSignatureException()


def check_token(token):
    return re.match('^[A-Za-z0-9]{3,32}$', token)


def generate_token(length=''):
    if not length:
        length = random.randint(3, 32)
    length = int(length)
    assert 3 <= length <= 32
    token = []
    letters = 'abcdefghijklmnopqrstuvwxyz' \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '0123456789'
    for _ in range(length):
        token.append(random.choice(letters))
    return ''.join(token)


def pay_sign_dict(appid, pay_sign_key, add_noncestr=True, add_timestamp=True, add_appid=True, **kwargs):
    """
    支付参数签名
    """
    assert pay_sign_key, "PAY SIGN KEY IS EMPTY"

    if add_appid:
        kwargs.update({'appid': appid})

    if add_noncestr:
        kwargs.update({'noncestr': generate_token()})

    if add_timestamp:
        kwargs.update({'timestamp': int(time.time())})

    params = kwargs.items()

    _params = [(k.lower(), v) for k, v in kwargs.items() if k.lower() != "appid"] + [('appid', appid), ('appkey', pay_sign_key)]
    _params.sort()

    sign = hashlib.sha1('&'.join(["%s=%s" % (str(p[0]), str(p[1])) for p in _params])).hexdigest()
    sign_type = 'SHA1'

    return dict(params), sign, sign_type


def json_loads(s):
    s = to_text(s)
    return json.loads(s)


def json_dumps(d):
    return json.dumps(d)


def to_text(value, encoding='utf-8'):
    """Convert value to unicode, default encoding is utf-8

    :param value: Value to be converted
    :param encoding: Desired encoding
    """
    if not value:
        return ''
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def to_binary(value, encoding='utf-8'):
    """Convert value to binary string, default encoding is utf-8

    :param value: Value to be converted
    :param encoding: Desired encoding
    """
    if not value:
        return b''
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return six.binary_type(value)


string_types = (six.string_types, six.text_type, six.binary_type)


def is_string(value):
    return isinstance(value, string_types)
