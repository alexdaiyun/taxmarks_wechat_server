# -*- coding:utf-8 -*-
"""
    weixinApi.replies
    ~~~~~~~~~~~~~~~~~~
    This module defines all kinds of replies you can send to WeiXin

"""
__author__ = 'alexday'



import time
import six

from .fields import StringField, IntegerField, ImageField
from .fields import VoiceField, VideoField, MusicField, ArticlesField
from .messages import BaseMessage, MessageMetaClass
from .utils import to_text, to_binary


REPLY_TYPES = {}


def register_reply(reply_type):
    def register(cls):
        REPLY_TYPES[reply_type] = cls
        return cls
    return register


class BaseReply(six.with_metaclass(MessageMetaClass)):
    """Base class for all replies"""
    source = StringField('FromUserName')
    target = StringField('ToUserName')
    time = IntegerField('CreateTime', int(time.time()))
    type = 'unknown'

    def __init__(self, **kwargs):
        self._data = {}
        message = kwargs.pop('message', None)
        if message and isinstance(message, BaseMessage):
            if 'source' not in kwargs:
                kwargs['source'] = message.target
            if 'target' not in kwargs:
                kwargs['target'] = message.source
            if hasattr(message, 'agent') and 'agent' not in kwargs:
                kwargs['agent'] = message.agent
        if 'time' not in kwargs:
            kwargs['time'] = int(time.time())
        for name, value in kwargs.items():
            field = self._fields.get(name)
            if field:
                self._data[field.name] = value
            else:
                raise AttributeError('Unknown argument: {arg}'.format(
                    arg=name
                ))

    def render(self):
        """Render reply from Python object to XML string"""
        tpl = u'<xml>\n{data}\n</xml>'
        nodes = []
        msg_type = u'<MsgType><![CDATA[{msg_type}]]></MsgType>'.format(
            msg_type=self.type
        )
        nodes.append(msg_type)
        for name, field in self._fields.items():
            value = getattr(self, name, field.default)
            node_xml = field.to_xml(value)
            nodes.append(node_xml)
        data = '\n'.join(nodes)
        return tpl.format(data=data)

    def __str__(self):
        if six.PY2:
            return to_binary(self.render())
        else:
            return to_text(self.render())


@register_reply('text')
class TextReply(BaseReply):
    """
    文本回复
    详情请参阅 http://mp.weixin.qq.com/wiki/index.php?title=发送被动响应消息
    """
    type = 'text'
    content = StringField('Content')


@register_reply('image')
class ImageReply(BaseReply):
    """
    图片回复
    详情请参阅 http://mp.weixin.qq.com/wiki/index.php?title=发送被动响应消息
    """
    type = 'image'
    image = ImageField('Image')

    @property
    def media_id(self):
        return self.image

    @media_id.setter
    def media_id(self, value):
        self.image = value


@register_reply('voice')
class VoiceReply(BaseReply):
    """
    语音回复
    详情请参阅 http://mp.weixin.qq.com/wiki/index.php?title=发送被动响应消息
    """
    type = 'voice'
    voice = VoiceField('Voice')

    @property
    def media_id(self):
        return self.voice

    @media_id.setter
    def media_id(self, value):
        self.voice = value


@register_reply('video')
class VideoReply(BaseReply):
    """
    视频回复
    详情请参阅 http://mp.weixin.qq.com/wiki/index.php?title=发送被动响应消息
    """
    type = 'video'
    video = VideoField('Video', {})

    @property
    def media_id(self):
        return self.video.get('media_id', None)

    @media_id.setter
    def media_id(self, value):
        video = self.video
        video['media_id'] = value
        self.video = video

    @property
    def title(self):
        return self.video.get('title', None)

    @title.setter
    def title(self, value):
        video = self.video
        video['title'] = value
        self.video = video

    @property
    def description(self):
        return self.video.get('description', None)

    @description.setter
    def description(self, value):
        video = self.video
        video['description']
        self.video = video


@register_reply('music')
class MusicReply(BaseReply):
    """
    音乐回复
    详情请参阅 http://mp.weixin.qq.com/wiki/index.php?title=发送被动响应消息
    """
    type = 'music'
    music = MusicField('Music', {})

    @property
    def thumb_media_id(self):
        return self.music.get('thumb_media_id', None)

    @thumb_media_id.setter
    def thumb_media_id(self, value):
        music = self.music
        music['thumb_media_id'] = value
        self.music = music

    @property
    def title(self):
        return self.music.get('title', None)

    @title.setter
    def title(self, value):
        music = self.music
        music['title'] = value
        self.music = music

    @property
    def description(self):
        return self.music.get('description', None)

    @description.setter
    def description(self, value):
        music = self.music
        music['description'] = value
        self.music = music

    @property
    def music_url(self):
        return self.music.get('music_url', None)

    @music_url.setter
    def music_url(self, value):
        music = self.music
        music['music_url'] = value
        self.music = music

    @property
    def hq_music_url(self):
        return self.music.get('hq_music_url', None)

    @hq_music_url.setter
    def hq_music_url(self, value):
        music = self.music
        music['hq_music_url'] = value
        self.music = music


@register_reply('news')
class ArticlesReply(BaseReply):
    """
    图文回复
    详情请参阅 http://mp.weixin.qq.com/wiki/index.php?title=发送被动响应消息
    """
    type = 'news'
    articles = ArticlesField('Articles', [])

    def add_article(self, article):
        if len(self.articles) == 10:
            raise AttributeError("Can't add more than 10 articles"
                                 " in an ArticlesReply")
        articles = self.articles
        articles.append(article)
        self.articles = articles


@register_reply('transfer_customer_service')
class TransferCustomerServiceReply(BaseReply):
    """
    将消息转发到多客服
    详情请参阅 http://mp.weixin.qq.com/wiki/index.php?title=将消息转发到多客服
    """
    type = 'transfer_customer_service'


def create_reply(reply, message=None, render=False):
    """
    Create a reply quickly
    """
    r = None
    if isinstance(reply, BaseReply):
        r = reply
        if message:
            r.source = message.target
            r.target = message.source
    elif isinstance(reply, six.string_types):
        r = TextReply(
            message=message,
            content=reply
        )
    elif isinstance(reply, (tuple, list)):
        if len(reply) > 10:
            raise AttributeError("Can't add more than 10 articles"
                                 " in an ArticlesReply")
        r = ArticlesReply(
            message=message,
            articles=reply
        )
    if r and render:
        return r.render()
    return r

