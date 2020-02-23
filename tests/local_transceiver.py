#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hmap.transceiver import Transceiver


class LocalTransceiver(Transceiver):
    """
    Interacts with other transceivers on the same thread and process. 
    LocalTransceiver is not thread-safe and is intended for testing purposes: 
    spoofing up interactions between subscribers, publishers, and routers
    """

    def __init__(self):
        super().__init__()
        self._connections = []

    @staticmethod
    def connect(nodes=[], **kwargs):
        """
        Connect two components that can use transceivers

        Args:
            u: component 1
            v: component 2
        """
        connections = LocalTransceiver.get_connections(len(nodes), **kwargs)
        for n, t in zip(nodes, connections):
            n.use(t)

    @staticmethod
    def get_connections(size: int):
        """
        Creates a fully connected network of local transceivers

        Args:
            size: desired number of transceivers in fully-connected-network

        Returns:
            (list): list of LocalSocket instances all interconnected
        """
        connections = [LocalTransceiver() for _ in range(size)]
        for t_i in connections:
            for t_j in connections:
                if t_i is not t_j:
                    t_i._connect(t_j)
        return connections

    @property
    def connections():
        """
        Tuple list of connections
        """
        return self._connections

    def _connect(self, connection: Transceiver):
        """
        Connects one local transceiver to another. The connection is one-way.

        Args:
            connection: transceiver connecting to
        """
        self._connections.append(connection)

    def transmit(self, data: bytes):
        """
        Iterates through all connections and invokes their receive methods with 
        a probability corresponding to the socket
        """
        for t in self._connections:
            t.receive(data)
