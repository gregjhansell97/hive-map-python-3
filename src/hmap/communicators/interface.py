#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface for all different communication paradigms
"""

from abc import ABC, abstractmethod
import math


class Transceiver(ABC):
    """
    TODO: better explanation
    """
    def __init__(self, uid=None):
        self._uid = uid
        # raw data delivered to callback with transceiver delivering it
        self._callbacks = []

    # can get implemented in subclass
    @property
    def message_size(self):
        return math.inf
    
    def transmit(self, data):
        """
        Actual transmission: needs to have raw-bytes header, I'm thinking
        something similar to udp protocol, maybe do a crc check
        """
        # raise some error if broadcast does not have a context...
        pass
    def receive(self, data):
        """
        FULL message gets delivered here
        """
        pass

    def deliver(self, data):
        pass

    # must be implemented in subclass
    @abstractmethod
    def broadcast(self, data):
        """
        """
        raise NotImplementedError
