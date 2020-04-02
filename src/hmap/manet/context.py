#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Provides standard way protocol developers interact with information provided
by user, TODO in-depth description
"""


class Context:
    def __init__(
            self, 
            uid=None, 
            routing_protocol="Flood",
            message_style="PySerializer",
            topic_style="StringHierarchy"):
        # 1. attempt to import and initialize if items are strings
        # 2. set field variables
        self.protocol = protocol
        self.msg_handler = msg_handler
        self.topic_handler = topic_handler
        # Use topic handler to serialize/deserialize topic, get subscriptions
        # subscription determines subscription is interested in topic
        # should be able to merge subscriptions (to optimize later)

    def Router(self, *args, **kwargs):
        return self.protocol.get_router(*args, **kwargs)


