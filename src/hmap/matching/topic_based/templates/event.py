#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching.topic_based import abc

def template(Topic, Msg):
    """Many Topic and Msg combinations cannot write them all out, template
    function creates event classes of a certain Topic and Msg type
    """
    with template.lock:
        if (Topic, Msg) in template.event_templates:
            return template.event_templates[(Topic, Msg)]

    class E(abc.TopicBasedEvent):
        """Event for all topic-based algorithms"""
        def __init__(self, targs, margs):
            super().__init__(Topic(targs), Msg(margs))
        @classmethod
        def serialize(cls, event):
            #TODO
            msg_serial = Msg.serialize(self.__msg)
            topic_serial = Topic.serialize(self.__topic)
            max_size = Topic.max_size #TODO
            # tack on size of topic to front
            return max_size + topic_serial + msg_serial
        @classmethod
        def deserialize(cls, raw_bytes, lazy=False):
            # TODO
            topic_size = raw_bytes[:Topic.max_size] #TODO
            raw_bytes = raw_bytes[Topic.max_size:] #TODO 
            self.__topic = Topic.deserialize(raw_bytes[:topic_size])
            self.__msg = Topic.deserialize(raw_bytes[topic_size:])
    with template.lock:
        if (Topic, Msg) not in template.event_templates:
            template.event_templates[(Topic, Msg)] = E
    return template.event_templates[(Topic, Msg)]

template.event_templates = {}
template.lock = Lock()
