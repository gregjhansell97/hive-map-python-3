#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from functools import reduce
import struct
from threading import Lock

from hmap.matching import abc

class TopicBasedSub(abc.Sub):
    Topic = None
    def __init__(self, tcontent, callback, topic=None):
        # topic arg lets me deserialize
        super().__init__()
        self.__topic = topic
        if self.__topic is None:
            self.__topic = self.Topic(tcontent)
        self.__callback = callback
    @property
    def callback(self):
        return self.__callback
    @property
    def topic(self):
        return self.__topic
    def calcsize(self):
        return self.__topic.calcsize()
    @classmethod
    def serialize(cls, subscription):
        return cls.Topic.serialize(subscription.__topic)
    @classmethod
    def deserialize(cls, raw_bytes, lazy=False):
        t = cls.Topic.deserialize(raw_bytes)
        return cls(None, None, topic=t)  # no callback
    def notify(self, event):
        # subscription can't call None
        if self.__callback is None:
            return
        self.__callback(event.topic.content, event.msg.content)

class HashableTopicBasedSub(TopicBasedSub):
    """TODO DESCRIPTION"""
    Topic = None
    class Collection(TopicBasedSub.Collection):
        Sub = None
        Topic = None
        def __init__(self):
            super().__init__()
            # dictionary of sets refering to specific subscriptions
            self.__table = defaultdict(set)
            self.__size = 4 # 4-bytes to store length of rest
            self.__numsubs = 0 
            self.__lock = Lock()

        def __iter__(self):
            return iter(
                reduce(set.union, self.__table.values(), set())
            )

        def calcsize(self):
            return self.__size

        def extend(self, sub_collection):
            # sets take care of duplicate subscription problem :)
            with self.__lock:
                for topic, subs in sub_collection.__table.items():
                    # need to calc_size here
                    self.__table[topic].update(subs)

        def matches(self, event):
            return self.__table[event.topic.content]

        def add(self, s):
            if s in self.__table[s.topic.content]:
                return 
            with self.__lock:
                self.__table[s.topic.content].add(s)
                # attempt to add to set first
                self.__size += s.calcsize()
                self.__numsubs += 1

        def remove(self, s):
            with self.__lock:
                self.__table[s.topic.content].remove(s)
                # attempt removal then add
                self.__size -= s.calcsize()
                self.__numsubs -= 1
        @classmethod
        def serialize(cls, collection):
            raw_data = struct.pack("I", collection.__numsubs)
            for s in collection:
                raw_data += cls.Sub.serialize(s)
            return raw_data
        @classmethod
        def deserialize(cls, raw_data, lazy=False):
            subs_remaining, = struct.unpack_from("I", raw_data, offset=0)
            raw_data = raw_data[struct.calcsize("I"):]
            col = cls()
            while subs_remaining > 0:
                s = cls.Sub.deserialize(raw_data)
                raw_data = raw_data[s.calcsize():]
                col.add(s)
                subs_remaining -= 1
            return col


