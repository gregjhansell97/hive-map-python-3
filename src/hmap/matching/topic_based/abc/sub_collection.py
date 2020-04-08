#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from threading import Lock

from hmap.matching import abc


class TopicBasedSubCollection(abc.SubCollection):
    def __init__(self):
        # dictionary of sets refering to specific subscriptions
        self.__table = defaultdict(set)

    def __iter__(self):
        return iter(
            reduce(lambda set1, set2: set1 + set2, self.__table.values())
        )

    def extend(self, sub_collection):
        self.__table
        # sets take care of duplicate subscription problem :)
        for topic, subs in sub_collection.__table:
            self.__table[topic].update(subs)

    def matches(self, event):
        return self.__table[event.topic]

    def add(self, s):
        self.__table[s.topic].add(s)

    def remove(self, subscription):
        self.__table[s.topic].remove(s)
