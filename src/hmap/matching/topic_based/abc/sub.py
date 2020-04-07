#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching import abc

class TopicBasedSub(abc.Sub):
    """TODO DESCRIPTION"""
    def __init__(self, topic, callback):
        super().__init__()
        self.__topic = topic
        self.__callback = callback
    @property
    def callback(self):
        return self.__callback
    @property
    def topic(self):
        return self.__topic
    def notify(self, event):
        # subscription can't call None
        if self.__callback is None:
            return
        self.__callback(event.topic.expose(), event.msg.expose())

