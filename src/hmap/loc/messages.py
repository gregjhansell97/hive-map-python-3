#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.messages import AbstractHeader

class LocHeader(AbstractHeader):
    """
    Supports meta information for messages from both location and destination
    instances

    Attributes:
        type(int): indicates kind of message: can either be PUB or ACK
        distance(int): distance away (in hops) of sender of message
        id(int): message id, which is ideally unique
    """
    PUB = 0
    ACK = 1
    def __init__(self, type_: int, distance: int, header_id: int):
        self.type = type_
        self.distance = min(distance, 0xFF)
        self.id = header_id
    @staticmethod
    def fmt():
        return "2BI"
    @property
    def data(self):
        return (self.type, self.distance, self.id)
