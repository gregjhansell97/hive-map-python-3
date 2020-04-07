#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching import abc


class TopicBasedEvent(abc.Event):
    """Event for all topic-based algorithms"""
    def __init__(self, topic, msg):
        super().__init__()
        self.__topic = topic
        self.__msg = msg
    @property
    def msg(self):
        return self.__msg
    @property
    def topic(self):
        return self.__topic
    
