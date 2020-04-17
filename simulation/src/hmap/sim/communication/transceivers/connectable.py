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
        self.__close_trigger, self.__close_flag = Pipe()
    def transmit(self, data, timeout=None):
        for p in self.__pipes:
            p.send(data)
    def recv(self, timeout=None):
        # timeout in-accurate when looping
        if self.__close_flag.poll() or self.__connections is None:
            # file has been closed
            raise EOFError
        while True:
            if len(self.__pipes) == 0: 
                return b""
            try:
                ready_pipes = wait(
                        self.__pipes | {self.__close_flag}, 
                        timeout=timeout)
            except OSError: # socket is closed done reading
                raise EOFError
            # timeout:
            if self.__close_flag in ready_pipes:
                raise EOFError
            if len(ready_pipes) == 0:
                return b""
            # no-timeout:
            for p in ready_pipes:
                try:
                    data = p.recv() 
                except EOFError:
                    self.__pipes.remove(p) # pipe no longer works
                    p.close()
                else:
                    return data
    def close(self):
        super().close()
        self.__close_trigger.close()
        self.__connections = None
        if self.__pipes is not None:
            for p in self.__pipes:
                p.close()
            self.__pipes = None
    def connect(self, trx):
        try:
            connection = self.__connections[trx]
            connection.poll() # see if OSError is raised
        except (KeyError, OSError): # trx not in connections or pipe is closed
            connection, trx_connection = Pipe()
            self.__connections[trx] = connection
            trx.__connections[self] = trx_connection
        except TypeError: 
            # close was invoked and __connections doesn't work
            raise EOFError
        try:
            self.__pipes.add(connection)
        except AttributeError:
            # close was invoked and __pipes set to None
            raise EOFError
            
    def disconnect(self, trx):
        # TODO disconnect not threadsafe
        try:
            connection = self.__connections[trx]
            self.__pipes.remove(connection)
        except KeyError:
            pass # connection not available or already removed
        except (AttributeError, TypeError):
            # __connections or __pipes is None 
            raise EOFError
