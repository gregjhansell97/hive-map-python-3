#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod
import struct

from hmap.matching.topic_based.abc import HashableTopic


class FlatNumber(HashableTopic):
    fmt = ""

    def __init__(self, content):
        # TODO move to super class (FlatNumber)
        self.__raw = struct.pack(self.fmt, content)
        self.__content = content

    @property
    def content(self):
        return self.__content

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

# hide parent class
__all__ = ["FlatByte", "FlatUByte", "FlatInt", "FlatUInt"]
