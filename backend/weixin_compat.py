# -*- coding: utf-8 -*-
__author__ = 'alexday'

from werkzeug.urls import url_parse, url_encode


def fixup_weixin_oauth(weixin):
    """Fixes the nonstandard OAuth interface of Tencent WeChat."""

    original_methods = {
        'authorize': weixin.authorize,
        'authorized_response': weixin.authorized_response,
    }

    def authorize(*args, **kwargs):
        response = original_methods['authorize'](*args, **kwargs)
        url = url_parse(response.headers['Location'])
        args = url.decode_query()

        # replace the nonstandard argument
        args['appid'] = args.pop('client_id')
        # replace the nonstandard fragment
        url = url.replace(query=url_encode(args), fragment='wechat_redirect')

        response.headers['Location'] = url.to_url()
        return response

    def authorized_response(*args, **kwargs):
        original_access_token_params = weixin.access_token_params
        weixin.access_token_params = {
            'appid': weixin.consumer_key,
            'secret': weixin.consumer_secret,
        }
        response = original_methods['authorized_response'](*args, **kwargs)
        weixin.access_token_params = original_access_token_params
        return response

    weixin.authorize = authorize
    weixin.authorized_response = authorized_response