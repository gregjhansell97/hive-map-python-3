#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from multiprocessing.pool import ThreadPool
import random

import pytest

from hmap.matching.topic_based import Matcher, Topic, Msg

def test_notify(FTopicBasedMatcher):
    subs = FTopicBasedMatcher.subscriptions(10)
    events = FTopicBasedMatcher.events(30)
    for e in events:
        s = random.choice(subs)
        s.notify(e)
        assert s.callback.log[-1] == (e.topic.content, e.msg.content)
def test_topic_preservation(FTopicBasedSubscription):
    S = FTopicBasedSubscription.Type
    subs = FTopicBasedSubscription.instances(10)
    topics = FTopicBasedSubscription.topics(10)
    # topics can be accessed
    for s, t in zip(subs, topics):
        assert s.topic == t.content

def test_template_algorithm_failures(FTopic, FMsg):
    T = FTopic.Type
    M = FMsg.Type
    T_str = T.__name__
    M_str = M.__name__
    # confirm invalid requests
    with pytest.raises(TypeError):
        algo = Matcher("invalid-topic", M)
    with pytest.raises(TypeError):
        algo = Matcher(T, "invalid-msg")
    # should not have name collisions across messages and topics!
    with pytest.raises(TypeError):
        algo = Matcher(M_str, M)
    with pytest.raises(TypeError):
        algo = Matcher(T, T_str)
    with pytest.raises(TypeError):
        algo = Matcher(int, M) # not of the right type
    with pytest.raises(TypeError):
        algo = Matcher(T, int) # not of the right type
    # NonHashableTopics Not supported yet
    class NotHashable(Topic):
        def content(self):
            return "daemon the koala"
    with pytest.raises(TypeError):
        algo = Matcher(NotHashable, M)

def test_algorithm_initialization(FTopic, FMsg):
    T = FTopic.Type
    M = FMsg.Type
    T_str = T.__name__
    M_str = M.__name__
    # requested by string yields same result as by class
    assert Matcher(T, M) == Matcher(T_str, M_str)

    # confirm multithreaded correct
    def thread_func(uid):
        algo = Matcher(T, M)
        return (algo.Subscription, algo.Event, algo.Interest)
    with ThreadPool(4) as p:
        classes = p.map(thread_func, [uid for uid in range(5)])
        assert(len(set(classes)) == 1)

