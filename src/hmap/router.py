#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Facilitates routing published messages to interested subscribers

Example:
    from hmap import Router
    r = Router()

Todo:
    * write Subscriber.transceiver setter
    * default handler, serializer, uid
"""

class Router:
    """Responsible for routing published messages to subscribers"""

    def __init__(
            self, 
            uid=None,
            heartbeat_rate=0.0,
            topic_handler=None,
            msg_serializer=None,
            transceiver=None):
        """
        Args:
            uid(bytes): Unique identifier
            heartbeat_rate(float): allowable synchronization transmissions rate
            topic_handler(TopicHandler): Handles serialization and comparason
                of topics
            msg_serializer(MsgSerializer): Serializes messages
            transceiver(Transceiver): Transceiver used to transmit and 
                receive data
        """
        self._uid = uid
        self._hbeat = heartbeat_rate
        self._topic_handler = topic_handler
        self._msg_serializer = msg_serializer
        self._trx = transceiver
        raise NotImplementedError

    @property
    def uid(self):
        """bytes: Unique identifier"""
        return self._uid

    @property
    def transceiver(self);
        """Transceiver: Transceiver used to transmit data"""
        return self._trx
    @self.transceiver.setter
    def transceiver(self, trx):
        raise NotImplementedError

    @property
    def heartbeat_rate(self):
        return self._hbeat
