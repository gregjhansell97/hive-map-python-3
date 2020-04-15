#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from abc import ABC, abstractmethod


class ITransceiver(ABC):
    def __init__(self, trx=None):
        super().__init__()
        self.__trx = None
        self.transceiver = trx

    @property
    def transceiver(self):
        """Transceiver used to transmit and receive data"""
        return self.__trx

    @transceiver.setter
    def transceiver(self, trx):
        if not self.is_valid_transceiver(trx):
            raise ValueError("incompatable transceiver")
        # check if already bound to transceiver
        if trx is self.__trx:
            return
        # unsubscribe old trx
        if self.__trx is not None:
            self.__trx.unsubscribe(self.on_transceiver_recv)
        # change transceiver
        self.__trx = trx
        # add new receiver callback
        if self.__trx is not None:
            self.__trx.subscribe(self.on_transceiver_recv)

    def is_valid_transceiver(self, trx):
        return True

    @abstractmethod
    def on_trx_recv(self, trx, raw_data):
        """Callback for transceivers to invoke when new messages are received

        Args:
            trx(Transceiver): receiver of message
            raw_data(bytes): bytes received 
        """
        raise NotImplementedError
