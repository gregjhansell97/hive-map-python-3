#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from threading import Lock

from hmap.matching.topic_based import abc

def template(Topic):
    with template.lock:
        if Topic in template.templates:
            return template.templates[Topic]
    # TODO will only work for flat structures
    class SC(abc.TopicBasedSubCollection):
        @classmethod
        def serialize(subscription):
            # TODO
            #return Topic.serialize(self.__topic)
            return b''
        @classmethod
        def deserialize(raw_bytes):
            # TODO
            return SC()
    with template.lock:
        if Topic not in template.templates:
            template.templates[Topic] = SC
    return template.templates[Topic]


template.templates = {}
template.lock = Lock()
