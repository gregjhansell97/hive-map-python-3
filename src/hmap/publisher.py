#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Facilitates publishing

Example:
    from hmap import Publisher
    p = Publisher()
    p.publish("weather.vt.killington", "rainy")

Todo:
    * write Publisher.publish implementation
    * default handler, serializer, transceiver, id
"""

import uuid


class Publisher:
    """Responsible for publishing information using transceivers provided"""

    def __init__(
            self, 
            uid=None,
            topic_handler=None, 
            msg_serializer=None, 
            transceiver=None):
        """
        Args:
            uid(bytes): Unique identifier of publisher
            topic_handler(TopicHandler): Handles serialization and comparason
                of topics. Must be consistent throughout hivemap infrastructure
            msg_serializer(MsgSerializer): Serializes messages. Must be
                consistent throughout hivemap infrastructure
            transceiver(Transceiver): Transceiver used to transmit data

        Raises:
            ValueError: argument types are not followed
        """
        # TODO: check types
        self._uid = uid
        self._topic_handler = topic_handler
        self._msg_serializer= msg_serializer
        self._trx = transceiver
        raise NotImplementedError

    @property
    def uid(self):
        """bytes: Unique identifier of publisher"""
        return self._uid
    @property
    def transceiver(self):
        """Transceiver: Transceivers used to transmit data"""
        return self._trx
    @self.transceiver.setter
    def transceiver(self, trx):
        raise NotImplementedError

    def publish(self, topic, data):
        """Publish data of a certain topic

        Args:
            topic: topic to publish data to
            data: information being published
        """
        # TODO
        raise NotImplementedError
