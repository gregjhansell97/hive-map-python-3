#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching import abc
import hmap.matching.topic_based.templates.event as event
import hmap.matching.topic_based.templates.sub as sub
import hmap.matching.topic_based.topic_types as topic_types
import hmap.matching.topic_based.msg_types as msg_types


def template(Topic, Msg):
    """TODO WRITE ABOUT
    """
    # import topics if not explicitly given
    if type(Topic) is str:
        try:
            Topic = getattr(topic_types, Topic)
        except AttributeError:
            raise TypeError("invalid topic type")
    if type(Msg) is str:
        try:
            Msg = getattr(msg_types, Msg)
        except AttributeError:
            raise TypeError("invalid topic type")

    class Algorithm(abc.Algorithm):
        def __init__(self):
            self.__E = event.template(Topic, Msg)
            self.__S = sub.template(Topic)
        @property
        def Event(self):
            return self.__E
        @property
        def Sub(self):
            return self.__S

    with template.lock:
        # because access to templates is not thread-safe
        return Algorithm()

template.lock = Lock()
