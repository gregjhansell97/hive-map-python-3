#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching import abc


class TopicBasedEvent(abc.Event):
    """Event for all topic-based algorithms"""

    Topic = None
    Msg = None

    def __init__(self, targs, margs, topic=None, msg=None):
        super().__init__()
        self.__topic = topic
        if self.__topic is None:
            self.__topic = self.Topic(targs)

        self.__msg = msg
        if self.__msg is None:
            self.__msg = self.Msg(margs)

    def calcsize(self):
        return self.topic.calcsize() + self.msg.calcsize()

    @property
    def msg(self):
        return self.__msg

    @property
    def topic(self):
        return self.__topic

    @classmethod
    def serialize(cls, event):
        raw_data = cls.Topic.serialize(event.topic)
        raw_data += cls.Msg.serialize(event.msg)
        return raw_data

    @classmethod
    def deserialize(cls, raw_bytes, lazy=False):
        t = cls.Topic.deserialize(raw_bytes, lazy)
        offset = t.calcsize()
        m = cls.Msg.deserialize(raw_bytes[:offset], lazy)
        return cls(None, None, topic=t, msg=m)

        raise NotImplementedError
