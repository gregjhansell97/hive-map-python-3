#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from multiprocessing.pool import ThreadPool
import random

import pytest

from hmap.matching import TopicBased

def test_notify(FTopicBasedAlgorithm):
    subs = FTopicBasedAlgorithm.subs(10)
    events = FTopicBasedAlgorithm.events(30)
    for e in events:
        s = random.choice(subs)
        s.notify(e)
        assert s.callback.log[-1] == (e.topic.content, e.msg.content)

def test_notify_serialized_copy(FTopicBasedAlgorithm):
    Sub = FTopicBasedAlgorithm.instances(1)[0].Sub
    serialize = Sub.serialize
    deserialize = Sub.deserialize
    subs = [deserialize(serialize(s)) for s in FTopicBasedAlgorithm.subs(10)]
    events = FTopicBasedAlgorithm.events(30)
    for e in events:
        s = random.choice(subs)
        s.notify(e)
        assert s.callback is None

def test_template_invocations(FTopic, FMsg):
    T = FTopic.InstanceType
    M = FMsg.InstanceType
    T_str = T.__name__
    M_str = M.__name__

    # confirm invalid requests
    with pytest.raises(TypeError):
        algo = TopicBased("invalid-topic", M)
    with pytest.raises(TypeError):
        algo = TopicBased(T, "invalid-msg")
    # should not have name collisions across messages and topics!
    with pytest.raises(TypeError):
        algo = TopicBased(M_str, M)
    with pytest.raises(TypeError):
        algo = TopicBased(T, T_str)
    with pytest.raises(TypeError):
        algo = TopicBased(int, M) # not of the right type
    with pytest.raises(TypeError):
        algo = TopicBased(T, int) # not of the right type
    
    def equal(a1, a2):
        return a1.Sub == a2.Sub and a1.Event == a2.Event
    # requested by string yields same result as by class
    assert equal(
            TopicBased(T, M), 
            TopicBased(T_str, M_str))

    # confirm multithreaded correct
    def thread_func(uid):
        algo = TopicBased(T, M)
        return (algo.Sub, algo.Event)
    with ThreadPool(4) as p:
        classes = p.map(thread_func, [uid for uid in range(5)])
        assert(len(set(classes)) == 1)

def test_hashable_topic_based_sub_collection(FHashableTopicBasedAlgorithm):
    algo = FHashableTopicBasedAlgorithm.instances(1)[0]
    subs = FHashableTopicBasedAlgorithm.subs(10)
    events = FHashableTopicBasedAlgorithm.events(30)
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
    for s in subs[:len(subs)//2]:
       col.remove(s)
    for s in subs[:len(subs)//2]:
       with pytest.raises(KeyError):
           col.remove(s)
    remaining = set(subs[len(subs)//2:])
    for e in events:
        matches = col.matches(e)
        expected = subs_dict[e.topic.content] & remaining
        assert len(matches) == len(expected)
        assert set(matches) == expected


    



