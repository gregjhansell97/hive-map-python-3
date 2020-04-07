#!/usr/bin/env python
# -*- coding: utf-8 -*-


from hmap.matching.topic_based.abc.msg import Msg

class PyObject(Msg):
    def __init__(self, o):
        self.__o = o
        pass
    def expose(self):
        return self.__o
    @staticmethod
    def serialize(instance):
        return b''
    @staticmethod
    def deserialize(instance, lazy=False):
        return PyObject(None)
