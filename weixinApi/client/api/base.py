# -*- coding: utf-8 -*-

__author__ = 'alexday'


class BaseWeiXinClientAPI(object):
    """ weixin Client API base class """

    def __init__(self, client):
        """
        Init with WeiXinClient object

        :param client: An instance of WeiXinClient
        """
        self._client = client

    def _get(self, url, **kwargs):
        return self._client._get(url, **kwargs)

    def _post(self, url, **kwargs):
        return self._client._post(url, **kwargs)

    @property
    def access_token(self):
        return self._client.access_token
