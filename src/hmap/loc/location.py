#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict, deque
import struct

from hmap.loc.messages import LocHeader

class Location:
    """
    Locations await messages delivered to them using the sockets provided. When
    a message is received, the bytes are delivered to appropriate subscribers
    """

    def __init__(self, id_: int):
        self._sockets = set()
        self._subscribers = set()
        self._id = id_
        # prevents redundant messages being received
        self._rcvd_msg_ids = deque(maxlen=10)
    @property
    def id(self):
        """
        Unique id of location that destinations use for their target
        """
        return self._id


    def subscribe(self, callback):
        """
        Given a callback subscribe the callback to receive bytes published to
        this location

        Args:
            callback: function/method invoked when message matching class is
                delivered to this location. A callback should take in only the
                bytes of the Location
        """
        self._subscribers.add(callback)

    def use(self, socket):
        """
        Uses a provided socket to interact with a network. Use is not 
        one-to-one. A location can use multiple sockets and a socket can be
        used by multiple locations. A location cannot use a socket more than 
        once

        Args:
            socket(hmap.network.Socket): socket used by destination

        Raises:
            ValueError: attempting to use socket more than once
        """
        if socket in self._sockets:
            raise ValueError
        socket._subscribe(self._id, self._deliver)
        self._sockets.add(socket)

    def _deliver(self, socket, topic: int, data: bytes):
        """
        Handles logistics of data received by this location

        Args:
            socket(hmap.network.AbstractSocket): socket invoking this _deliver
                method
            topic: topic of item deliverd (it should match id)
            data: data received by location. Can receive a location
                message that needs to be forwarded or receive an ack mesage that
                adjusts the reliabliity
        """
        # handles logistics of data received by socket (must mirror destination
        # class in order to duck type
        h, b = LocHeader.deserialize(data)
        if h.type == LocHeader.PUB:
            # filter out already received messages
            if h.id in self._rcvd_msg_ids:
                return
            # valid publish header, send acknowledgment and then process body
            self._rcvd_msg_ids.append(h.id)
            ack_h = LocHeader(LocHeader.ACK, 0, h.id)
            ack_b = struct.pack("B", 255) # pack in probability
            socket._publish(self._id, LocHeader.serialize(ack_h, ack_b))
            # invoke all callbacks
            for cb in self._subscribers:
                cb(b)
