#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pipe
from multiprocessing.connection import wait

from hmap.interface.communication import Transceiver


class ConnectableTransceiver(Transceiver):
    def __init__(self):
        super().__init__()
        self.__pipes = set()
        self.__connections = {}
    def transmit(self, data, timeout=None):
        for p in self.__pipes:
            p.send(data)
    def recv(self, timeout=None):
        # timeout in-accurate when looping
        while True:
            if len(self.__pipes) == 0: 
                return b""
            ready_pipes = wait(self.__pipes, timeout=timeout)
            # timeout:
            if len(ready_pipes) == 0:
                return b""
            # no-timeout:
            for p in ready_pipes:
                try:
                    data = p.recv() 
                except EOFError:
                    self.__pipes.remove(p) # pipe no longer works
                else:
                    return data
    def close(self):
        super().close()
        self.__connections.clear()
        for p in self.__pipes:
            p.close()
        self.__pipes.clear()
    def connect(self, trx):
        try:
            connection = self.__connections[trx]
        except KeyError: # trx not in connections
            connection, trx_connection = Pipe()
            self.__connections[trx] = connection
            trx.__connections[self] = trx_connection

        self.__pipes.add(connection)
            
    def disconnect(self, trx):
        # TODO disconnect not threadsafe
        try:
            connection = self.__connections[trx]
            self.__pipes.remove(connection)
        except KeyError:
            pass # connection not available or already removed
