#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""
from functools import partial
from multiprocessing.pool import ThreadPool

import pytest

from hmap.matching.topic_based.templates.event import template as event_template

def test_content_retrival(TopicBasedEventFixture):
    TBEF = TopicBasedEventFixture
    for t, m in zip(TBEF.topics, TBEF.msgs):
        e = TBEF.Event(t, m)
        assert e.topic.content == t
        assert e.msg.content == m

def test_templates(FlatIntTopicFixture, PyObjMsgFixture):
    T = FlatIntTopicFixture.Topic
    M = PyObjMsgFixture.Msg
    with ThreadPool(2) as p:
        event_classes = p.map(partial(event_template, T), [M for _ in range(5)])
        assert(len(set(event_classes)) == 1)

