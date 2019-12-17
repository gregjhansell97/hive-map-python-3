#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from hmap.messages import Msg
from hmap.network.messages import SocketHeader


class AbstractSocket(ABC):
    """
    Base class enforces 'proper' socket protocol. A socket overrides one
    method: broadcast. The broadcast method sends bytes of data to other sockets
    on the network. Upon receiving data, a socket must invoke this base classes
    deliver method. Sockets are used internally by location and destination
    instances: facilitates the communication agnostic behavior of the location
    and destination. TL;DR: override broadcast method, use (do not override)
    deliver method.
    """

    def __init__(self):
        self._callbacks = dict() # key is topic, value is callback

    def _subscribe(self, topic: int, cb):
        """
        Subscribes a callback to the topic specified, there can only be one
        subscriber per topic.

        Args:
            topic: topic being subscribed to
            cb: callback invoked when info of a topic is recieved; cb takes in
                the topic value and data published
        """
        if topic in self._callbacks:
            raise ValueError("topic already subscribed")
        self._callbacks[topic] = cb

    def _publish(self, topic: int, msg: bytes):
        """
        Publishes a message to a specific topic. If there is a subscriber for
        that topic then the message will be delivered to that subscriber.

        Args:
            topic: topic being published to
            msg: raw bytes being published
        """
        h = SocketHeader(0xAB, 0xCD, topic)
        msg = Msg(h, msg)
        self.broadcast(Msg.serialize(msg))

    def deliver(self, data: bytes):
        """
        Invoked by child class to deliver messages received to socket. Acts as
        the original event driver

        Args:
            data: raw bytes delivered to socket
        """
        msg = Msg.deserialize(SocketHeader, data)
        try:
            cb = self._callbacks[msg.header.topic]
        except KeyError:
            pass
        else:
            cb(self, msg.header.topic, msg.body)

    @abstractmethod
    def broadcast(self, data: bytes):
        """
        Bytes of data to send to all other reachable sockets in the network. 
        This call is non-blocking. Must be implemented by subclasses

        Args:
            data: raw bytes being broadcasted to all other endpoints
        """
        raise NotImplementedError
