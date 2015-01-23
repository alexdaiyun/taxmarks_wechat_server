# -*- coding:utf-8 -*-
__author__ = 'alexday'

from flask import Flask, abort, request, current_app

from weixinApi.exceptions import InvalidSignatureException
from weixinApi.utils import check_signature
from weixinApi import parse_message
from weixinApi.replies import *
from weixinApi.events import *

from config import Config
from . import api


@api.errorhandler(404)
def error_not_found(error):
    return abort(404)


# 公众号消息服务器网址接入验证
# 需要在公众帐号管理台手动提交, 验证后方可接收微信服务器的消息推送


# 接收用户消息入口
# 每次接收消息均需要验证
@api.route('/weixin', methods=['GET', 'POST'])
def weixin():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')

    current_app.logger.debug('[/weixin] signature:%s  timestamp:%s  nonce:%s  echostr:%s ' %
                             (signature, timestamp, nonce, echo_str))

    try:
        check_signature(Config.MP_CONFIG['MP_TOKEN_KEY'], signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        return echo_str
    if request.method == 'POST':
        current_app.logger.debug('[POST /weixin] %s' % request.data)
        message = parse_message(request.data)
        reply = process_message_type(message)
        return reply


def process_route(message):
    # TODO：处理消息路由

    return None


help_text_bak01 = \
    u"""
    亲，欢迎关注税签服务号。在此，您可以获取最新、最快的税务资讯，还可直接点击下方工具栏“法规库”，直接输入文号、文件名或者是法规内容（同时输入多个关键字也行哦），即可随时随刻快速查询税务、海关及外汇法规，畅享移动查询之便捷，亦或是点击下方工具栏“微社区”与小伙伴们一起聊聊税，侃侃山。如您对税签有任何问题、建议或反馈，可在本页面直接回复，我们的客服小签将会为您细心解答。
    """

help_text = \
    u"""
    亲，欢迎关注税签服务号。在这里，您可以获取最新、最快的税务资讯，也可直接点击下方工具栏“知识地图”，随时随刻快速查询税务、海关及外汇法规，亦或是点击下方工具栏“微社区”与小伙伴们一起聊聊税，侃侃山。如果您是税签专家版的付费用户，还可直接在移动端查询知识点，非付费用户也可申请试用一个月。如您对税签有任何问题、建议或反馈，可在本页直接回复，我们的客服小签将会为您细心解答。
    """


def process_message_type(message):
    if message.type == 'text':
        reply = process_text(message)
    elif message.type == 'event':
        reply = process_event(message)
    elif message.type == 'voice':
        # reply = process_voice(message)
        reply = None
    elif message.type == 'image':
        # reply = process_image(message)
        reply = None
    else:
        # reply = create_reply('Sorry, can not handle this for now，这是个测试版', message)
        # 默认转到多客服
        reply = process_customer_service(message)
    return reply.render()


def process_event(message):
    if message.event == 'subscribe':
        reply = create_reply(help_text, message)
    elif message.event == 'click':
        reply = process_click_event(message)
    elif message.event == 'view':
        # reply = create_reply(u'view event, 收到你的消息了，谢谢', message)
        reply = None
    else:
        reply = None

    return reply


def process_click_event(message):
    reply = None
    if message.key == 'bind_weixin':
        msg_text = u'你好，欢迎访问税签。' \
                   u'<a href=\'%s/wx_auth_redirect?menucode=101\' >请点击绑定</a>' % \
                   (Config.APP_CONFIG['MP_SERVER_HOST'])

        reply = create_reply(msg_text, message)
    elif message.key == 'wenda_post':
        reply = create_reply(u'click event, eventkey: wenda_post', message)
    else:
        reply = create_reply(u'click event', message)

    return reply


def process_text(message):
    if message.content == u'?' or message.content == u'? ':
        # reply = create_reply('这是一个测试版', message)
        reply = help_info(message)
        # reply = process_customer_service(message)
    else:
        # reply = create_reply(message.content, message)
        # 默认转到多客服
        reply = process_customer_service(message)
    return reply


def process_image(message):
    msg_text = u'image message event, 收到你的消息了，谢谢'
    reply = TextReply(
        message=message,
        content=msg_text
    )
    return reply


def process_voice(message):
    msg_text = u'voice message event, 收到你的消息了，谢谢'
    reply = TextReply(
        message=message,
        content=msg_text
    )
    return reply


def process_customer_service(message):
    reply = TransferCustomerServiceReply(
        message=message
    )
    current_app.logger.debug('process_customer_service %s' % reply)
    return reply


def help_info(message):

    reply = TextReply(
        message=message,
        content=help_text
    )

    return reply

# @app.route('/weixin', methods=['POST'])
# def weixin_message():
