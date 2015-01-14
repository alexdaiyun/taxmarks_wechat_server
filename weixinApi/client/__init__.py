# -*- coding:utf-8 -*-
__author__ = 'alexday'


from .base import BaseWeiXinClient
from . import api


class WeiXinClient(BaseWeiXinClient):
    """
    weixin API Client
    通过这个类可以操作微信 API的接口类型如下：
    （1）向用户发送消息
    （2）自定义菜单
    （3）用户管理
    """
    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'

    def __init__(self, appid, secret, access_token=None):
        self.appid = appid
        self.secret = secret
        self._access_token = access_token
        self.expires_at = None

        # APIs
        self.menu = api.WeiXinMenu(self)
        self.message = api.WeXinMessage(self)
        self.media = api.WeiXinMedia(self)
        self.user = api.WeiXinUser(self)
        self.group = api.WeiXinGroup(self)

    def fetch_access_token(self):
        """
        获取 access token
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档

        :return: 返回的 JSON 数据包
        """
        return self._fetch_access_token(
            url='https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.secret
            }
        )