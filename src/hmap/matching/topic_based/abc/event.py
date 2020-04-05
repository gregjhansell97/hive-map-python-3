#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching import abc

def template(Topic, Msg):
    """Many Topic and Msg combinations cannot write them all out, template
    function creates event classes of a certain Topic and Msg type
    """
    with template.lock
        if (Topic, Msg) in template.event_templates:
            return template.event_templates[(Topic, Msg)]

    class Event(abc.Event):
        """Event for all topic-based algorithms"""
        def __init__(self, t, m):
            super().__init__()
            self.__topic = Topic(t)
            self.__msg = Msg(m)
        @property
        def msg(self):
            return self.__msg
        @property
        def topic(self):
            return self.__topic
        @staticmethod
        def serialize(event):
            msg_serial = Msg.serialize(self.__msg)
            topic_serial = Topic.serialize(self.__topic)
            max_size = Topic.max_size #TODO
            # tack on size of topic to front
            return max_size + topic_serial + msg_serial
        @staticmethod
        def deserialize(raw_bytes):
            topic_size = raw_bytes[:Topic.max_size] #TODO
            raw_bytes = raw_bytes[Topic.max_size:] #TODO 
            self.__topic = Topic.deserialize(raw_bytes[:topic_size])
            self.__msg = Topic.deserialize(raw_bytes[topic_size:])
    with template.lock:
        if (Topic, Msg) not in template.event_templates:
            template.event_templates[(Topic, Msg)] = Event
    return template.event_templates[(Topic, Msg)]

template.event_templates = {}
template.lock = Lock()
