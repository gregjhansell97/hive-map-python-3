#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from threading import Lock

from hmap.matching import abc

def template(Topic)
    with template.lock
        if Topic in template.templates:
            return template.templates[Topic]
    # TODO will only work for flat structures
    class Subscriptions(abc.Subscriptions):
        def __init__(self, t, cb):
            self.__s_table = defaultdict(list)
        def matches(self, event):
            return self.__s_table[event.topic]
        def on_add(self, subscription):
            self.__s_table[subscription.topic].append(subscription)
        def on_remove(self, subscription):
            self.__s_table[subscription.topic].remove(subscription)
        @staticmethod
        def serialize(subscription):
            return Topic.serialize(self.__topic)
        @staticmethod
        def deserialize(raw_bytes):
            self.__topic = Topic.deserialize(raw_bytes)
            self.__callback = None
    with template.lock:
        if Topic not in template.templates:
            template.templates[Topic] = Subscriptions
    return template.templates[Topic]


template.templates = {}
template.lock = Lock()
