#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.matching import abc

templates = {}
class Event(abc.Event):
    """Event for all topic-based algorithms"""
    Topic = None
    Msg = None

    def __init__(self, tcontent, mcontent, topic=None, msg=None):
        super().__init__()
        self.__topic = topic
        if self.__topic is None:
            self.__topic = self.Topic(tcontent)

        self.__msg = msg
        if self.__msg is None:
            self.__msg = self.Msg(mcontent)
    def __repr__(self):
        return f"({self.topic}, {self.msg})"

    def calcsize(self):
        return self.__topic.calcsize() + self.__msg.calcsize()

    @property
    def msg(self):
        return self.__msg

    @property
    def topic(self):
        return self.__topic

    @classmethod
    def serialize(cls, event):
        raw_data = cls.Topic.serialize(event.__topic)
        raw_data += cls.Msg.serialize(event.__msg)
        return raw_data

    @classmethod
    def deserialize(cls, raw_bytes, lazy=False):
        t = cls.Topic.deserialize(raw_bytes, lazy)
        offset = t.calcsize()
        m = cls.Msg.deserialize(raw_bytes[offset:], lazy)
        return cls(None, None, topic=t, msg=m)
    
    @staticmethod
    def template_class(T, M):
        """Many Topic and Msg combinations cannot write them all out, template
        function creates event classes of a certain Topic and Msg type
        NOT THREAD SAFE
        """
        if (T, M) in templates:
            return templates[(T, M)]
        class E(Event):
            """Event for all topic-based algorithms"""
            Topic = T
            Msg = M
        templates[(T, M)] = E
        return E
