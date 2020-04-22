#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Abstract base classes for communicator"""

from abc import ABC, abstractmethod
import atexit
import math
import select
import weakref


class Communicator(ABC):
    """Abstract base class for all communicators. Communicators send to one
    or more other communicators and receive data from one or more communicators.
    """
    __instances = []
    def __init__(self):
        Communicator.__instances.append(weakref.ref(self))
    def __del__(self): 
        self.close()

    @abstractmethod
    def send(self, data, timeout=None):
        """Sends data to one or more communicators
        
        Args:
            data(bytes): data to send to other communicators

        Raises:
            - if data is too large
            - if data are not bytes
            - if transceiver is closed while transmiting
            - if past timeout and couldn't send information
        """
        raise NotImplementedError

    @abstractmethod
    def recv(self, timeout=None):
        """Receives data from another communicator, blocks for duration of
        timeout. If timeout is set to None, then blocks indefinitely

        Args:
            timeout: duration of blocking call

        Returns:
            (bytes): data received

        Raises:
            - if there is too much data received
            - if transceiver is closed while receiving
            - if passed timeout and didn't receive any bytes
        """
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """
        Idempotent function that ends send and recv capabilities
        """
        raise NotImplementedError

    @atexit.register
    def __clean_up():
        comms = [t() for t in Communicator.__instances if t() is not None]
        for c in comms:
            c.close()
