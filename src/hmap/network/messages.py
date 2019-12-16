#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.messages import AbstractHeader


class SocketHeader(AbstractHeader):
    """
    Header information used to describe a socket-message. An important aspect
    of the socket-header is the allignment which checks the ordering of bytes
    delivered to ensure confirm correct ordering/no corruption
    """

    fmt = "2BI"
    allignment = 0xABCD

    def __init__(self, a_1: int, a_2: int, topic: int):
        assert self.allignment == (a_1 << 8) + a_2
        self.topic = topic

    @property
    def data(self):
        a_1 = 0xAB
        a_2 = 0xCD
        return (a_1, a_2, self.topic)
