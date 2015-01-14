# -*- coding:utf-8 -*-
"""
    weixinApi.exceptions
    ~~~~~~~~~~~~~~~~~~~~
    Basic exceptions definition.

"""
__author__ = 'alexday'

import six

from .utils import to_binary, to_text


class WeiXinException(Exception):
    """Base exception for weixinApi"""

    def __init__(self, errcode, errmsg):
        """
        :param errcode: Error code
        :param errmsg: Error message
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        if six.PY2:
            return to_binary('Error code: {code}, message: {msg}'.format(
                code=self.errcode,
                msg=self.errmsg
            ))
        else:
            return to_text('Error code: {code}, message: {msg}'.format(
                code=self.errcode,
                msg=self.errmsg
            ))


class WeiXinClientException(WeiXinException):
    """weixin API client exception class"""
    pass


class InvalidSignatureException(WeiXinException):
    """Invalid signature exception class"""

    def __init__(self, errcode=-40001, errmsg='Invalid signature'):
        super(InvalidSignatureException, self).__init__(errcode, errmsg)


class APILimitedException(WeiXinException):
    """weixin API call limited exception class"""

    def __init__(self, errcode=45009, errmsg='api freq out of limit'):
        super(APILimitedException, self).__init__(errcode, errmsg)


class InvalidAppIdException(WeiXinException):
    """Invalid app_id exception class"""

    def __init__(self, errcode=-40005, errmsg='Invalid AppId'):
        super(InvalidAppIdException, self).__init__(errcode, errmsg)


class WeiXinOAuthException(WeiXinException):
    """weixin OAuth API exception class"""
    pass