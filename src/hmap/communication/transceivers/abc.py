#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Abstract base classes for transceivers"""

from abc import ABC, abstractmethod
import math


class Transceiver(ABC):
    """Abstract base class for all transceivers. Transceivers are event-driven;
    callbacks are invoked upon receiving a transmission
    """

    def __init__(self):
        # raw data delivered to callback with transceiver delivering it
        self.__callbacks = []  # callback(trx, data)

    @abstractmethod
    def transmit(self, data):
        """Transmits data to other transceivers listening
        
        Args:
            data(bytes): data to transmit on network
        """
        pass

    def receive(self, data):
        """Receives data from another transceiver

        Args:
            data(bytes): data received from a correspond transmit from another
                transceiver
        """
        for cb in self.__callbacks:
            cb(self, data)

    def subscribe(self, callback):
        """Registers a callback to the transceiver that gets invoked when a
        message is received
        
        Args:
            callback: a callback to be invoked on new data reception
        """
        if callback in self.__callbacks:
            return
        self.__callbacks.append(callback)

    def unsubscribe(self, callback):
        """Removes callback from list of on data reception callbacks

        Args:
            callback: callback to be removed
        """
        self.__callbacks.remove(callback)


# TODO write a base class for packing a message
