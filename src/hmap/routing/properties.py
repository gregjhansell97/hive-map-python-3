#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sched
import time

from abc import ABC, abstractmethod

class TransceiverProperty(ABC):
    def __init__(self, trx=None):
        super().__init__()
        self.__trx = None
        self.transceiver = trx
    @property
    def transceiver(self):
        """Transceiver used to transmit and receive data"""
        return self.__trx
    @self.transceiver.setter
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


# TODO: initial heartbeat is 0.0, heartbeat is cancelled when set to 0.0
class HeartbeatProperty(ABC):
    def __init__(self,*, max_heartbeat_rate):
        super().__init__()
        if heartbeat_rate < 0.0:
            raise ValueError("heartbeat rate must be positive")
        self.__max_hbeat = max_heartbeat_rate
        self.__hbeat = 0.0
        self.__hbeat_scheduler = None
        self.__cancel_loop = None
        # schedule item in initializer
        # TODO handle async heartbeat
        
        if heartbeat_rate > 0.0:
            self.__hbeat_scheduler = sched.scheduler(time.time, time.sleep)
            self.__cancel_loop = self.__hbeat_scheduler.enter(
                    1.0/self.__hbeat,
                    1,
                    self.__hbeat_loop)
    def __hbeat_loop(self):
        # TODO: check if event already scheduled (prevent backing up)
        scheduler.enter(1.0/self.__hbeat, 1, self.__hbeat_loop)
        # may run into some logging errors
        self.on_heartbeat()
    @property
    def heartbeat_rate(self):
        """Heartbeat rate used by router"""
        return self.__hbeat
    @heartbeat_rate.setter
    def heartbeat_rate(self, hbeat):
        if hbeat > self.__max_hbeat:
            raise ValueError("heartbeat rate too fast")
        self.__hbeat = hbeat
    @abstractmethod
    def on_hearbeat(self):
        """Periodically invoked based on heartbeat parameter"""
        raise NotImplementedError 

class ContextProperty(ABC):
    def __init__(self, context=None):
        super().__init__()
        if not self.is_valid_context(context):
            raise ValueError("invalid context")
        self.__context = context
    @property
    def context(self):
        """Context read-only property"""
        return self.__context
    def is_valid_context(self, ctx):
        return True
