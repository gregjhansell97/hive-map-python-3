#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching import abc
import hmap.matching.topic_based.templates.event as event
import hmap.matching.topic_based.templates.sub as sub
import hmap.matching.topic_based.templates.sub_collection as scollection
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

    # try to get from already made templates
    with template.lock:
        if (Topic, Msg) in template.algorithm_templates:
            return template.algorithm_templates[(Topic, Msg)]

    # could not find already made template, must make one
    class Algorithm(abc.Algorithm):
        @property
        def Event(self):
            return event.template(Topic, Msg)

        @property
        def Sub(self):
            return sub.template(Topic)

        @property
        def SubCollection(self):
            return scollection.template(Topic)

    with template.lock:
        if (Topic, Msg) not in template.algorithm_templates:
            template.algorithm_templates[(Topic, Msg)] = Algorithm()
    return template.algorithm_templates[(Topic, Msg)]


template.algorithm_templates = {}
template.lock = Lock()
