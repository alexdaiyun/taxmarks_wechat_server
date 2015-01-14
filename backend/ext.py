# -*- coding: utf-8 -*-
__author__ = 'alexday'

from flask_oauthlib.client import OAuth

from .weixin_compat import fixup_weixin_oauth

# app.config['WEIXIN'] = dict(
#     consumer_key=MP_AppID,
#     consumer_secret=MP_AppSecret
# )

oauth = OAuth()
weixin = oauth.remote_app(
    'weixin',
    app_key='WEIXIN',
    request_token_params={'scope': 'snsapi_base'},
    base_url='https://api.weixin.qq.com',
    authorize_url='https://open.weixin.qq.com/connect/oauth2/authorize',
    access_token_url='https://api.weixin.qq.com/sns/oauth2/access_token',
    # important: ignore the 'text/plain' said by weixin api and enforce the
    #            response be parsed as json.
    content_type='application/json',
)
fixup_weixin_oauth(weixin)