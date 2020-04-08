#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import struct

from hmap.matching.topic_based.abc.msg import Msg


class PyObj(Msg):
    def __init__(self, o):
        self.__o = o
        self.__raw = None

    def expose(self):
        return self.__o

    def calcsize(self):
        return len(self.__raw)

    @classmethod
    def serialize(cls, m):
        if m.__raw is None:
            m.__raw = pickle.dumps(m.__o)
        return m.__raw

    @staticmethod
    def deserialize(raw_data, lazy=False):
        m = PyObj(pickle.loads(raw_data))
        m.__raw = raw_data  # added optimization
        return m
