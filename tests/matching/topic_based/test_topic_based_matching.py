#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing.pool import ThreadPool
import random

from hmap.matching.topic_based.templates.event import template as event_template
from hmap.matching.topic_based.templates.sub import template as sub_template

def test_notify(FTopicBasedSub, FTopicBasedEvent):
    subs = FTopicBasedSub.instances()
    events = FTopicBasedEvent.instances()
    for e in events:
        s = random.choice(subs)
        s.notify(e)
        assert s.callback.log[-1] == (e.topic.content, e.msg.content)

def test_multi_threaded_template_invocations(FFlatInt, FPyObj):
    T = FFlatInt.InstanceType
    M = FPyObj.InstanceType
    def thread_func(uid):
        return (sub_template(T), event_template(T, M))
    with ThreadPool(4) as p:
        classes = p.map(thread_func, [uid for uid in range(5)])
        assert(len(set(classes)) == 1)
