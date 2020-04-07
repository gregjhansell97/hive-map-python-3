#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching.topic_based import abc


def template(Topic):
    """Many Topic combinations cannot write them all out, template function 
    creates subscription classes of a certain Topic 
    """
    with template.lock:
        if Topic in template.subscription_templates:
            return template.subscription_templates[Topic]

    class Subscription(abc.TopicBasedSub):
        """TODO DESCRIPTION"""
        def __init__(self, targs, cb):
            super().__init__(Topic(targs), cb)
        @staticmethod
        def serialize(subscription):
            return Topic.serialize(self.__topic)
        @staticmethod
        def deserialize(raw_bytes, lazy=False):
            t = Topic.deserialize(raw_bytes)
            return Subscription(t, None) # no callback 
    with template.lock:
        if Topic not in template.subscription_templates:
            template.subscription_templates[Topic] = Subscription
    return template.subscription_templates[Topic]

template.subscription_templates = {}
template.lock = Lock()

