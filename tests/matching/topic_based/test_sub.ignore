#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for FlatInt matching.TopicBased algorithm
"""

from collections import defaultdict
import math
import pytest

from hmap import matching

from tests.fixtures import Callback
from tests.matching.topic_based.fixtures import MatchingAlgorithm


def test_sub(MatchingAlgorithm, Callback):
    """Verifies subscription is notified properly"""
    Sub, Event, SubCollection = MatchingAlgorithm
    cb = Callback

    # initialization, topic=1 callback=cb
    s = Sub(1, cb)
    assert s.callback is cb
    assert s.topic == 1

    e = Event(1, "msg1")
    s.notify(e)
    # should still be notified even if event is not matching
    e = Event(2, "msg2")
    s.notify(e)
    assert cb.log == {(2, "msg2"), (1, "msg1")} == s.callback.log


'''
def test_subscriptions(FlatNumber):
    """Verifies add and remove features of subscriptions"""
    A = get_matching_algorithm(FlatNumber)
    S, E, SCollection = (A.Sub, A.Event, A.SubCollection)

    # Subscriptions instance
    scollection = SCollection()
    # Separate datastructure to track Subscriptions
    subscriptions = defaultdict(lambda: [])
    # iterate through and create n subscriptions for each topic number n
    for i in range(10):
        for topic in range(i):
            s = S(topic, get_callback())
            subscriptions[topic].append(s)
            scollection.add(s)
    # notify all subscribers that match an event
    for topic in range(10):
        e = E(topic, "msg")
        for s in scollection.matches(e):
            # go through all matching subscriptions and notify them
            s.notify(e)
    # TODO check iter works appropriately
    # confirm only correct subscriptions were notified
    for topic in range(10):
        for s in subscriptions[topic]:
            assert s.callback.log == {(topic, "msg")}
      

    # test callback property
    cb = get_callback()
    s = Sub(2, cb)

    # callback is stored correctly
    assert s.callback == cb
    assert s.topic == 2

    # pass in events
    for i in range(10):
        e = Event(i, "msg")
        s.notify(e)
        assert s.callback.log == {(e.topic.expose(), e.msg.expose())}
        s.callback.log = set()

    # can be in a set
    subscriptions = set([s])
'''
