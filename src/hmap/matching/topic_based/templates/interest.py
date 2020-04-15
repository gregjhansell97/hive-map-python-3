#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
from threading import Lock

from hmap.matching import abc, topic_based
from hmap.matching.topic_based.abc import HashableTopic

templates = {}

class Interest(abc.Interest):
    Topic = None
    def __init__(self, topics):
        super().__init__()
        # TODO potentially remove overlaping topics
        self.__topics = topics
    @property
    def topics(self):
        return self.__topics
    def calcsize(self):
        size = struct.calcsize("I")
        for t in self.__topics:
            size += t.calcsize()
        return size
    @classmethod
    def serialize(cls, interest):
        data = struct.pack("I", len(interest.__topics))
        for t in interest.__topics:
            data += cls.Topic.serialize(t)
        return data
    @classmethod
    def deserialize(cls, raw_bytes):
        topics_len, = struct.unpack_from("I", raw_bytes, offset=0)
        # shift raw bytes up
        raw_bytes = raw_bytes[struct.calcsize("I"):]
        topics = []
        for _ in range(topics_len):
            t = cls.Topic.deserialize(raw_bytes)
            raw_bytes = raw_bytes[t.calcsize():]
            topics.append(t)
        return cls(topics)
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
        topics = [t for t in self.__table.keys()]
        if len(topics) > 0:
            return iter([self.Interest(topics)])
        return []
    def match(self, event):
        try:
            return iter(self.__table[event.topic])
        except KeyError:
            return iter([])
    def add(self, interest, val):
        with self.__lock:
            for t in interest.topics:
                try:
                    self.__table[t].append(val)
                except KeyError:
                    self.__table[t] = [val]
    def remove(self, interest, val):
        with self.__lock:
            for t in interest.topics:
                try:
                    self.__table[t].remove(val)
                    if len(self.__table[t]) == 0:
                        # empty list, no longer interested
                        del self.__table[t]
                except ValueError:
                    raise KeyError
