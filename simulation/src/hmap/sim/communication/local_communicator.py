#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pipe
from multiprocessing.connection import wait
import select
from threading import Lock

from hmap.interface.communication import Communicator
from hmap.interface.communication.traits import Pollable


class LocalCommunicator(Communicator, Pollable):
    def __init__(self):
        super().__init__()
        # locks write pipe
        self.__address_lock = Lock()
        self.__neighbors_lock = Lock()
        # one way pipe R, W
        self.__closed = False
        self.__mailbox, self.__address = Pipe(False) 
        self.__neighbors = set()
    def send(self, data, timeout=None):
        closed_neighbors = []
        with self.__neighbors_lock:
            if self.__closed:
                raise EOFError # self is closed
            # iterate through neighbors and deliver data to them
            for n in self.__neighbors:
                try:
                    n.deliver(data)
                except (OSError, EOFError): # node is closed
                    closed_neighbors.append(n)
            # remove closed neighbors
            for n in closed_neighbors:
                self.__neighbors.remove(n)
    def deliver(self, data):
        if self.__closed:
            raise EOFError
        with self.__address_lock:
            if select.select([], [self.__address], [], 0) != []:
                # can send bytes on pipe
                self.__address.send_bytes(data)
    def recv(self, timeout=None):
        # timeout in-accurate when looping
        if self.__neighbors is None:
            raise EOFError
        try:
            if self.__mailbox.poll(timeout=timeout): # poll mailbox
                # theres something in the mail!
                return self.__mailbox.recv_bytes()
            else: # timeout ended
                return b"" # not data received
        except (OSError, EOFError):
            raise EOFError # socket is closed
    def close(self):
        self.__closed = True
        self.__address.close()
    def send_filenos(self):
        return ([], [self.__address], []) # always ready to send!
    def recv_filenos(self):
        return ([self.__mailbox], [], [])
    def connect(self, comm):
        if self.__closed:
            raise EOFError
        with self.__neighbors_lock:
            self.__neighbors.add(comm)
    def disconnect(self, comm):
        with self.__neighbors_lock:
            try:
                self.__neighbors.remove(comm)
            except KeyError:
                pass # if you couldn't remove it don't worry
