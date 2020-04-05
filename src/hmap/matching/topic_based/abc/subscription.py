#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching import abc


def template(Topic):
    """Many Topic combinations cannot write them all out, template function 
    creates subscription classes of a certain Topic 
    """
    with template.lock:
        if Topic in template.subscription_templates:
            return template.subscription_templates[Topic]

    class Subscription(abc.Subscription)
        """TODO DESCRIPTION"""
        def __init__(self, t, cb):
            super().__init__()
            self.__topic = Topic(t)
            self.__callback = cb
        def notify(self, event):
            # subscription can't call None
            if self.__callback is None:
                return
            self.__callback(event.topic, event.msg)
        @staticmethod
        def serialize(subscription):
            return Topic.serialize(self.__topic)
        @staticmethod
        def deserialize(raw_bytes):
            self.__topic = Topic.deserialize(raw_bytes)
            self.__callback = None
    with template.lock:
        if Topic not in template.subscription_templates:
            template.subscription_templates[Topic] = Subscription
    return template.subscription_templates[Topic]

template.subscription_templates = {}
template.lock = Lock()

