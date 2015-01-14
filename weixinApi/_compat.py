# -*- coding:utf-8 -*-
"""
    weixinApi._compat
    This module makes it easy for weixinApi to run on both Python 2 and 3.
"""
__author__ = 'alexday'


import six
try:
    """ Use simplejson if we can, fallback to json otherwise. """
    import simplejson as json
except ImportError:
    import json


def byte2int(s, index=0):
    """Get the ASCII int value of a character in a string.

    :param s: a string
    :param index: the position of desired character

    :return: ASCII int value
    """
    if six.PY2:
        return ord(s[index])
    return s[index]