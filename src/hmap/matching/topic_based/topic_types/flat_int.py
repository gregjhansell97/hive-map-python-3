#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.matching.topic_based.abc.topic import Topic

class FlatInt(Topic):
    def __init__(self, topic):
        # TODO move to super class (FlatNumber)
        if type(topic) is not int:
            raise TypeError("invalid type, must be an integer")
        if -32769 > topic or topic > 32767:
            raise TypeError("topic must be an integer between -32769 & 32767")
        self.__topic = topic
    def __hash__(self):
        return hash(self.__topic)
    def __eq__(self, other):
        return self.__topic == other
    def expose(self):
        return self.__topic
    @staticmethod
    def serialize(instance):
        return b''
    @staticmethod
    def deserialize(instance, lazy=False):
        return FlatInt(0)

