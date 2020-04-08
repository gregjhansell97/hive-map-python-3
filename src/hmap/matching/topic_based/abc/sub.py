#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching import abc


class TopicBasedSub(abc.Sub):
    """TODO DESCRIPTION"""

    Topic = None

    def __init__(self, targs, callback, topic=None):
        # topic arg lets me deserialize
        super().__init__()
        self.__topic = topic
        if self.__topic is None:
            self.__topic = self.Topic(targs)
        self.__callback = callback

    @property
    def callback(self):
        return self.__callback

    @property
    def topic(self):
        return self.__topic

    def calcsize(self):
        return self.__topic.calcsize()

    def notify(self, event):
        # subscription can't call None
        if self.__callback is None:
            return
        self.__callback(event.topic.expose(), event.msg.expose())

    @classmethod
    def serialize(cls, subscription):
        return cls.Topic.serialize(self.__topic)

    @classmethod
    def deserialize(cls, raw_bytes, lazy=False):
        t = cls.Topic.deserialize(raw_bytes)
        s = cls(None, None, topic=t)
        return t  # no callback
