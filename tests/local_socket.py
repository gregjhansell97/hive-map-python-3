#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from hmap.sockets import AbstractSocket


class LocalSocket(AbstractSocket):
    """
    Interacts with other sockets on the same thread and process. LocalSocket is
    not thread-safe and is intended for testing purposes: spoofing up
    interactions between nodes
    """

    def __init__(self):
        super().__init__()
        self._sockets = []  # [(<LocalSocket>, <prob success>), ...]

    @staticmethod
    def connect(u, v):
        """
        Connect two components that can use a socket

        Args:
            u: component 1
            v: component 2
        """
        sockets = LocalSocket.get_sockets(2)
        u.use(sockets[0])
        v.use(sockets[1])


    @staticmethod
    def get_sockets(size: int, reliability: float = 1.0):
        """
        Creates a fully connected network of local sockets

        Args:
            size: number of sockets in inter-connected-socket-network
            reliability: probability of success that a message sent from one 
            socket gets to another socket

        Returns:
            (list): list of LocalSocket instances all interconnected
        """
        sockets = [LocalSocket() for _ in range(size)]
        for s_i in sockets:
            for s_j in sockets:
                if s_i is not s_j:
                    s_i.add_socket(s_j, reliability)
        return sockets

    @property
    def sockets():
        """
        Tuple list of sockets and their probability of successful sends
        """
        return self._sockets

    def add_socket(self, socket: AbstractSocket, prob: float):
        """
        Connects one local socket to another. The connection is one-way.

        Args:
            socket: socket connecting to
            prob: probability that messages sent to the socket will make it
        """
        self._sockets.append((socket, prob))

    def broadcast(self, data: bytes):
        """
        Iterates through all sockets and invokes their deliver methods with a
        probability corresponding to the socket
        """
        for s, prob in self._sockets:
            if random.random() < prob:
                s.deliver(data)
