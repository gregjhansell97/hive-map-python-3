#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        Topic = None
        def __init__(self):
            super().__init__()
            # dictionary of sets refering to specific subscriptions
            self.__table = defaultdict(set)

        def __iter__(self):
            return iter(
                reduce(lambda set1, set2: set1 + set2, self.__table.values())
            )

        def extend(self, sub_collection):
            # sets take care of duplicate subscription problem :)
            for topic, subs in sub_collection.__table:
                self.__table[topic].update(subs)

        def matches(self, event):
            return self.__table[event.topic]

        def add(self, s):
            self.__table[s.topic].add(s)

        def remove(self, subscription):
            self.__table[s.topic].remove(s)
        @classmethod
        def serialize(cls, collection):
            raise NotImplementedError #TODO
        @classmethod
        def deserialize(cls, raw_bytes, lazy=False):
            raise NotImplementedError #TODO


