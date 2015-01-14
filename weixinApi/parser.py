# -*- coding: utf-8 -*-
"""
    weixinApi.parser
    ~~~~~~~~~~~~~~~~
    This module provides functions for parsing WeiXin messages
"""

__author__ = 'alexday'

import xmltodict
# from xml.etree import ElementTree

from .messages import MESSAGE_TYPES, UnknownMessage
from .events import EVENT_TYPES
from .utils import to_text


def parse_message(xml):
    """
    Parse WeiXin XML format messages
    :param xml: XML format messages
    :return: Parsed messages or events
    """
    if not xml:
        return

    # message = dict((child.tag, to_text(child.text))
    #               for child in ElementTree.fromstring(xml))

    message = xmltodict.parse(to_text(xml))['xml']
    message_type = message['MsgType'].lower()
    if message_type == 'event':
        event_type = message['Event'].lower()
        if event_type == 'subscribe' and 'EventKey' in message and \
                message['EventKey']:
            # Scan to subscribe with scene id event
            event_type = 'subscribe_scan'
            message['Event'] = event_type
            message['EventKey'] = message['EventKey'].replace('qrscene_', '')
        message_class = EVENT_TYPES.get(event_type, UnknownMessage)
    else:
        message_class = MESSAGE_TYPES.get(message_type, UnknownMessage)
    return message_class(message)
