#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Abstract base classes for transceivers"""

from abc import ABC, abstractmethod
import math


class Transceiver(ABC):
    """Abstract base class for all transceivers. Transceivers transmit and
    receive data from neighboring transceivers.
    """

    @abstractmethod
    def transmit(self, data, timeout=None):
        """Transmits data to other transceivers within communication range
        
        Args:
            data(bytes): data to transmit on network

        Raises:
            - if data is too large
            - if data are not bytes
            - if transceiver is closed while transmiting
            - if past timeout and couldn't send information
        """
        raise NotImplementedError

    @abstractmethod
    def recv(self, timeout=None):
        """Receives data from another transceiver, blocks for duration of
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
        Idempotent function that ends transmission and reception capabilities
        """
        pass
    @property
    def recv_strength(self):
        """Number between 0 and 1, a higher number indicates better message
        transmission detection"""
        return 1
    @recv_strength.setter
    def set_recv_strength(self, rcv_strength):
        raise AttributeError
    @property
    def transmit_strength(self):
        """Number between 0 and 1, a higher number indicates a more robust
        signal that is likely to reach more transceivers"""
        return 1
    @transmit_strength.setter
    def set_transmit_strength(self, tr_range):
        raise AttributeError

# TODO write a base class for packing a message
