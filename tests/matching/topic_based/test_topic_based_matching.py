#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from multiprocessing.pool import ThreadPool
import random

import pytest

from hmap.matching.topic_based.templates.event import template as event_template
from hmap.matching.topic_based.templates.sub import template as sub_template

def test_notify(FTopicBasedSub, FTopicBasedEvent):
    subs = FTopicBasedSub.instances()
    events = FTopicBasedEvent.instances()
    for e in events:
        s = random.choice(subs)
        s.notify(e)
        assert s.callback.log[-1] == (e.topic.content, e.msg.content)

def test_notify_serialized_copy(FTopicBasedSub, FTopicBasedEvent):
    Sub = FTopicBasedSub.InstanceType
    serialize = Sub.serialize
    deserialize = Sub.deserialize
    subs = [deserialize(serialize(s)) for s in FTopicBasedSub.instances()]
    events = FTopicBasedEvent.instances()
    for e in events:
        s = random.choice(subs)
        s.notify(e)
        assert s.callback is None

def test_multi_threaded_template_invocations(FFlatInt, FPyObj):
    T = FFlatInt.InstanceType
    M = FPyObj.InstanceType
    def thread_func(uid):
        return (sub_template(T), event_template(T, M))
    with ThreadPool(4) as p:
        classes = p.map(thread_func, [uid for uid in range(5)])
        assert(len(set(classes)) == 1)

def test_hashable_topic_based_sub_collection(FHashableTopicBasedAlgorithm):
    algo = FHashableTopicBasedAlgorithm.instances()[0]
    subs = FHashableTopicBasedAlgorithm.subs()
    events = FHashableTopicBasedAlgorithm.events()
    subs_count = len(subs)
    assert subs_count > 6, "insufficient number of subscribers"
    # arrange subs by topics
    subs_dict = defaultdict(set)
    for s in subs:
        # NOTE why we NEED hashable topics
        subs_dict[s.topic.content].add(s)
    col = algo.Sub.Collection()
    assert [] == [s for s in col]
    for s in subs:
        col.add(s)
    # check duplicates (YOSO - "You only subscripe once")
    for s in subs:
        col.add(s)
    for e in events:
        matches = col.matches(e)
        expected = subs_dict[e.topic.content]
        assert len(matches) == len(expected)
        assert set(matches) == expected
    for s in subs[:subs_count//2]:
       col.remove(s)
    for s in subs[:subs_count//2]:
       with pytest.raises(KeyError):
           col.remove(s)
    remaining = set(subs[subs_count//2:])
    for e in events:
        matches = col.matches(e)
        expected = subs_dict[e.topic.content] & remaining
        assert len(matches) == len(expected)
        assert set(matches) == expected


    



