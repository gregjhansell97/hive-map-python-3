#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import struct

from hmap.matching.topic_based.abc.msgs import Msg


class PyObj(Msg):
    def __init__(self, content):
        self.__content = content
        self.__raw = pickle.dumps(content)

    @property
    def content(self):
        return self.__content

    def calcsize(self):
        return len(self.__raw)

    @classmethod
    def serialize(cls, m):
        return m.__raw

    @staticmethod
    def deserialize(raw_data, lazy=False):
        m = PyObj(pickle.loads(raw_data))
        return m
