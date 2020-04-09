#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching.topic_based.abc import events


def template(T, M):
    """Many Topic and Msg combinations cannot write them all out, template
    function creates event classes of a certain Topic and Msg type
    """
    with template.lock:
        if (T, M) in template.event_templates:
            return template.event_templates[(T, M)]

    class E(events.TopicBasedEvent):
        """Event for all topic-based algorithms"""
        Topic = T
        Msg = M

    # make sure instance didn't get created while making E
    with template.lock:
        if (T, M) not in template.event_templates:
            template.event_templates[(T, M)] = E
    return template.event_templates[(T, M)]


template.event_templates = {}
template.lock = Lock()
