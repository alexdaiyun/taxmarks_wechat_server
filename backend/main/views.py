# -*- coding:utf-8 -*-
__author__ = 'alexday'

import os
from urllib import quote
from flask import current_app, render_template, jsonify, request, abort, make_response, redirect, json, url_for

from weixinApi.client import *
from weixinApi.oauth import *
from config import Config
from . import main


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@main.route('/')
def home():
    client = WeiXinClient(Config.MP_CONFIG['MP_AppID'], Config.MP_CONFIG['MP_AppSecret'])
    result = client.user.get_followers()

    openid_list = result['data']['openid']

    users = []

    pageIndex = 20

    i = 0
    for u_openid in openid_list:
        if i > pageIndex:
            pass
        else:
            try:
                result_user = client.user.get(u_openid)
                user = dict(nickname=result_user['nickname'], openid=result_user['openid'])
                # print(u'nickname: %s openid: %s' % (user['nickname'], user['openid']))
                users.append(user)
                i += 1
            except Exception:
                pass

    current_app.logger.debug(i)
    current_app.logger.debug('log debug: home page')
    # current_app.logger.info('log info: home page')
    # current_app.logger.exception('log exception: home page')

    return render_template('home/home.html', users=users)


@main.route('/login')
def login():
    return render_template('login/login.html')


@main.route('/help')
def page_help():
    return render_template('help/help.html')


@main.route('/user')
def page_user():
    client = WeiXinClient(Config.MP_CONFIG['MP_AppID'], Config.MP_CONFIG['MP_AppSecret'])
    result = client.user.get_followers()

    """
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    urlfile = os.path.join(SITE_ROOT, "static", "users_data.json")
    current_app.logger.debug(urlfile)

    r = open(urlfile)
    parsed_data = r.read()

    # Convert to String
    parsed_data = json.dumps(parsed_data)

    current_app.logger.debug(parsed_data)

    # Convert to JSON Object
    json_object = json.loads(parsed_data)

    current_app.logger.debug(json_object)

    json_object = json.loads(json_object)

    current_app.logger.debug(json_object)

    j_data_r = json_object['openid']  # j_data['openid']
    j = 0
    for u_openid in j_data_r:
        # app.logger.debug('%s %s' % (j, u_openid))
        j += 1

    openid_list = json_object['openid']

    """
    openid_list = result['data']['openid']

    users = []
    i = 0
    for u_openid in openid_list:

        try:
            result_user = client.user.get(u_openid)

            result_group = client.group.get(result_user['openid'])

            user = dict(nickname=result_user['nickname'],
                        openid=result_user['openid'],
                        groupid=result_group['groupid'])


            print(u'%s|%s|%s|%s' % (i,
                                    user['nickname'],
                                    user['openid'],
                                    user['groupid']))

            users.append(user)
            i += 1
        except Exception:
            pass

    # print(users)
    return render_template('user/user.html', users=users)


@main.route('/wx/authorization')
def wx_authorization():
    args = request.args
    openid = args.get('openid', '')

    current_app.logger.debug('wx_authorization()  openid: %s' % openid)

    return render_template('wx_auth/wx_auth.html')


# 预处理对用户执行微信oauth授权的引导
@main.route('/wx_auth_redirect')
def wx_auth_redirect():
    # 生成换取code的微信授权引导页

    # url = u'https://open.weixin.qq.com/connect/oauth2/authorize?' \
    # u'appid=wx3ef755a9cf4666ef' \
    #       u'&redirect_uri=http%3A%2F%2Fhelixappserver3.duapp.com%2Fwx_auth' \
    #       u'&response_type=code' \
    #       u'&scope=snsapi_base' \
    #       u'&state=STATE#wechat_redirect'

    args = request.args
    menucode = args.get('menucode', '')
    url = args.get('url', '')

    if menucode == '':
        redirect_url = Config.APP_CONFIG['MP_SERVER_HOST'] + u'/wx_auth'
    else:
        url = six.moves.urllib.parse.quote_plus(url)
        redirect_url = Config.APP_CONFIG['MP_SERVER_HOST'] + u'/wx_auth?menucode=%s&url=%s' % (menucode, url)

    # redirect_url = six.moves.urllib.parse.quote_plus(redirect_url)

    weixin_oauth = WeiXinOAuth(Config.MP_CONFIG['MP_AppID'],
                               Config.MP_CONFIG['MP_AppSecret'],
                               redirect_url,
                               'snsapi_base',
                               'STATE')
    weixinoauth_url = weixin_oauth.authorize_url

    return redirect(weixinoauth_url, code=302)


@main.route('/wx_auth')
def wx_auth():
    # 通过code换取微信的网页授权access_token
    # 使用snsapi_base方式时，也获得了openid

    # resp = createOauthUrlForCode('http://helixappserver3.duapp.com/wx_auth')
    resp = None
    openid = None
    access_token = None
    access_token_res = None

    args = request.args
    code = args.get('code', '')

    menucode = args.get('menucode', '')
    url = args.get('url', '')

    # 跳转页面默认值
    redirect_url = u''
    # 跳转页面根据menucode值进行设定
    if menucode == '201':
        redirect_url = Config.APP_CONFIG['WE_CENTER_HOST'] + u'/wecenter/'
    if menucode == '202':
        # 跳转到weCenter发布页面上
        redirect_url = Config.APP_CONFIG['WE_CENTER_HOST'] + u'/wecenter/?/m/publish/'
    if menucode == '100':
        redirect_url = url
    if menucode == '101':
        redirect_url = url

    redirect_url = six.moves.urllib.parse.quote_plus(redirect_url)

    weixin_oauth = WeiXinOAuth(Config.MP_CONFIG['MP_AppID'],
                               Config.MP_CONFIG['MP_AppSecret'],
                               '',
                               'snsapi_base',
                               'STATE')

    if code:
        # 用微信的code换取access_token, openid
        try:
            access_token_res = weixin_oauth.fetch_access_token(code)
            openid = access_token_res['openid']
            access_token = access_token_res['access_token']

            client = WeiXinClient(Config.MP_CONFIG['MP_AppID'], Config.MP_CONFIG['MP_AppSecret'])
            result_user = client.user.get(openid)
            wechat_user = []
            wechat_user = dict(subscribe=result_user['subscribe'],
                               nickname=result_user['nickname'],
                               openid=result_user['openid'],
                               headimgurl=result_user['headimgurl'],
                               subscribe_time=result_user['subscribe_time']
                               )

            current_app.logger.info(u'subscribe:%s | subscribe_time:%s  | nickname:%s | openid:%s | headimgurl:%s'
                                     % (wechat_user['subscribe'],
                                        wechat_user['subscribe_time'],
                                        wechat_user['nickname'],
                                        wechat_user['openid'],
                                        wechat_user['headimgurl']))

            # 默认跳转处理
            sso_redirect_url_list = [
                Config.APP_CONFIG['SSO_SERVER_HOST'],
                u'/SsoRedirect.aspx?',
                u'openid=',
                openid,
                u'&url=',
                redirect_url
            ]

            if menucode == '200':
                # 进入绑定页面
                sso_redirect_url_list = [
                    Config.APP_CONFIG['TAXMARKS_WEIXINWEB_HOST'],
                    u'/#/wx_bind?',
                    u'openid=',
                    openid,
                    u'&url=',
                    redirect_url
                ]
            if menucode == '100':
                # 税签微信版的SSO验证页面
                sso_redirect_url_list = [
                    Config.APP_CONFIG['TAXMARKS_WEIXINWEB_HOST'],
                    u'/#/wx/authorization?',
                    u'openid=',
                    openid,
                    u'&url=',
                    redirect_url
                ]
            if menucode == '101':
                # 税签微信版的SSO验证页面
                sso_redirect_url_list = [
                    Config.APP_CONFIG['TAXMARKS_WEIXINWEB_HOST'],
                    u'/#/wx_bind?',
                    u'openid=',
                    openid,
                    u'&url=',
                    redirect_url
                ]
                current_app.logger.debug(''.join(sso_redirect_url_list))

            return redirect(''.join(sso_redirect_url_list), code=302)

        except WeiXinOAuthException, e:
            resp = u'授权失败: errcode: %s errmsg: %s' % (e.errcode, e.errmsg)
            return resp
    else:
        resp = '授权失败，返回请重新尝试'
        return resp


@main.route('/weixinClient/api/v1.0/sendTextMessage', methods=['POST'])
def create_send_text_message():
    # print('this request.data:', request.data)
    if not request.json:
        abort(400)
    touser = request.json['touser']
    content = request.json['content']
    url = request.json['url']
    title = request.json['title']

    # print('touser:', touser)
    # print('content:', content)

    # if request.json not in request.json:
    # abort(400)
    # print(request.json)

    client = WeiXinClient(Config.MP_CONFIG['MP_AppID'], Config.MP_CONFIG['MP_AppSecret'])
    if url == "":
        result = client.message.send_text(touser, content)
    else:
        articles = [{
                        'title': title,
                        'description': content,
                        'url': url,
                        'image': ''
                    }]
        result = client.message.send_articles(touser, articles)

    return jsonify({'status': True, 'result': result})


@main.route('/weixinClient/api/v1.0/Menu', methods=['GET'])
def query_menu():
    client = WeiXinClient(Config.MP_CONFIG['MP_AppID'], Config.MP_CONFIG['MP_AppSecret'])
    result = client.menu.get()
    return jsonify({'status': True, 'result': result})


@main.route('/weixinClient/api/v1.0/Menu', methods=['POST'])
def create_menu():
    # print('this request.data:', request.data)
    if not request.json:
        abort(400)
    menu_data = json.dumps(request.json)
    menu_data = menu_data.decode('unicode_escape')
    # str_menu_data = u'%s' % menu_data
    # print(str_menu_data)
    # print(u'menu_data: %s' % menu_data)
    # reload(sys)
    # sys.setdefaultencoding('utf-8')

    client = WeiXinClient(Config.MP_CONFIG['MP_AppID'], Config.MP_CONFIG['MP_AppSecret'])
    result = client.menu.create(menu_data.encode('utf-8'))
    return jsonify({'status': True, 'result': result})


@main.route('/weixinClient/api/v1.0/Menu', methods=['DELETE'])
def delete_menu():
    client = WeiXinClient(Config.MP_CONFIG['MP_AppID'], Config.MP_CONFIG['MP_AppSecret'])
    result = client.menu.delete()
    return jsonify({'status': True, 'result': result})


@main.route('/weixinClient/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})




# def formatBizQueryParaMap(paraMap, urlencode):
#     """格式化参数，签名过程需要使用"""
#     slist = sorted(paraMap)
#     buff = []
#     for k in slist:
#         v = quote(paraMap[k]) if urlencode else paraMap[k]
#         buff.append("{0}={1}".format(k, v))
#
#     return "&".join(buff)
#
#
# def createOauthUrlForCode(redirectUrl):
#     """生成可以获得code的url"""
#     urlObj = {}
#     urlObj["appid"] = Config.MP_CONFIG['MP_AppID']
#     urlObj["redirect_uri"] = redirectUrl
#     urlObj["response_type"] = "code"
#     urlObj["scope"] = "snsapi_base"
#     urlObj["state"] = "STATE#wechat_redirect"
#     bizString = formatBizQueryParaMap(urlObj, False)
#     return "https://open.weixin.qq.com/connect/oauth2/authorize?" + bizString
#
#
# def example():
#     resp = u'this is example'
#     return resp


"""
微信授权处理页面说明：


/wx_auth_redirect
预处理对用户执行微信oauth授权的引导
用户被引导至/wx_auth
参数:
  menucode 功能代码 具体请见/wx_auth中的相应参数说明

/wx_auth
微信用户在微信中进行微信oauth授权处理页面
微信授权成功后获得code，利用code换取access_token，同时获得openid
根据menucode代码，执行相应的页面跳转
没有menucode参数时， 默认进入SSO验证页面  SsoRedirect.aspx
参数:
  menucode 功能代码
  200  进入绑定页面
  201  进入weCenter页面
  202  进入weCenter发布页面
  100  税签微信版的SSO验证页面
  101  税签微信版的绑定微信页面
  102  税签微信版的注册用户页面（同时绑定微信）


/wx/authorization 微信绑定验证 (暂不使用）
  openid   用户的openid
  url      需要跳转的页面
"""
