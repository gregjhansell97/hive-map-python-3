#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.communication.transceivers.abc import Transceiver

class LocalTransceiver(Transceiver):
    def __init__(self):
        super().__init__()
        self.__connections = set()
    def transmit(self, data):
        for t in self.__connections:
            t.receive(data)
    def connect(self, trx):
        if trx is self:
            return
        self.__connections.add(trx)
    def disconnect(self, trx):
        self.__connections.remove(trx)

