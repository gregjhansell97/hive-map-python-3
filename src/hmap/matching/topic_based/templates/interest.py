#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching import abc, topic_based
from hmap.matching.topic_based.abc import HashableTopic

templates = {}

class Interest(abc.Interest):
    Topic = None
    def __init__(self, topic):
        super().__init__()
        self.__topic = topic
    @property
    def topic(self):
        return self.__topic
    def calcsize(self):
        return self.__topic.calcsize()
    @classmethod
    def serialize(cls, interest):
        return cls.Topic.serialize(interest.__topic)
    @classmethod
    def deserialize(cls, raw_bytes):
        t = cls.Topic.deserialize(raw_bytes)
        return cls(t)
    class Map(abc.Interest.Map):
        Interest = None
    @staticmethod
    def template_class(T):
        if T in templates:
            return templates[T]
        if issubclass(T, HashableTopic):
            class I(Interest):
                class Map(HashMap):
                    pass
        else:
            raise TypeError(f"{T}'s default impl is not supported")
        # populate template variables
        I.Topic = T
        I.Map.Interest = I
        templates[T] = I
        return I

class HashMap(Interest.Map):
    def __init__(self):
        super().__init__()
        # dictionary refers to specific interests
        self.__table = dict()
        self.__lock = Lock()
    @property
    def interests(self):
        return iter([self.Interest(t) for t in self.__table.keys()])
    def match(self, event):
        try:
            return iter(self.__table[event.topic])
        except KeyError:
            return iter([])
    def add(self, interest, val):
        with self.__lock:
            try:
                self.__table[interest.topic].append(val)
            except KeyError:
                self.__table[interest.topic] = [val]
    def remove(self, interest, val):
        with self.__lock:
            try:
                self.__table[interest.topic].remove(val)
                if len(self.__table[interest.topic]) == 0:
                    # empty list, no longer interested
                    del self.__table[interest.topic]
            except ValueError:
                raise KeyError
