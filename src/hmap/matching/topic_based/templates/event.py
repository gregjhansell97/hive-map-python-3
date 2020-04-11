#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.matching.topic_based.abc.events import TopicBasedEvent
from hmap.matching.topic_based.abc.msgs import Msg as BaseMsg
from hmap.matching.topic_based.abc.topics import Topic as BaseTopic


def template(T, M):
    """Many Topic and Msg combinations cannot write them all out, template
    function creates event classes of a certain Topic and Msg type
    NOT THREAD SAFE
    """
    if not issubclass(M, BaseMsg): # topic checked by sub
        raise TypeError("invalid msg type")

    if (T, M) in template.event_templates:
        return template.event_templates[(T, M)]
    class E(TopicBasedEvent):
        """Event for all topic-based algorithms"""
        Topic = T
        Msg = M
    template.event_templates[(T, M)] = E
    return E


template.event_templates = {}
