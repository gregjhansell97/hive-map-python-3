#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class Transceiver(ABC):
    """
    """
    def __init__(self, uid=None, heartbeat_rate=0.0, context=None):
        self._hbeat=hearbeat_rate
        self._uid = uid
        self._context = context

    @property
    def context(self):
        raise NotImplementedError
    @context.setter
    def context(self, ctx):
        # context is gonna have to have a list of transceivers
        raise NotImplementedError

    def publish(self, topic, msg):
        raise NotImplementedError
    def subscribe(self, topic, callback):
        raise NotImplementedError

    @abstractmethod
    def transmit(self, data):
        pass
    def receive(self, data):
        pass
