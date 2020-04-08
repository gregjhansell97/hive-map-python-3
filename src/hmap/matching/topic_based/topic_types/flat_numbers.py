#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod
import struct

from hmap.matching.topic_based.abc.topic import Topic

class FlatNumber(Topic):
    fmt = ""
    def __init__(self, topic):
        # TODO move to super class (FlatNumber)
        self.__raw = struct.pack(self.fmt, topic) 
        self.__topic = topic
    def __hash__(self):
        return hash(self.__topic)
    def __eq__(self, other):
        return self.__topic == other
    def expose(self):
        return self.__topic
    def calcsize(self):
        return struct.calcsize(self.fmt)
    @classmethod
    def serialize(cls, instance):
        return instance.__raw
    @classmethod
    def deserialize(cls, raw_data, lazy=False):
        return cls(struct.unpack_from(cls.fmt, raw_data, offset=0)[0])
        # return remaining bytes

class FlatByte(FlatNumber):
    fmt = "b"

class FlatUByte(FlatNumber):
    fmt = "B"

class FlatInt(FlatNumber):
    fmt = "i"

class FlatUInt(FlatNumber):
    fmt = "I"

