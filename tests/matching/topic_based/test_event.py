#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from collections import defaultdict
import math
import pytest

from tests.matching.topic_based.fixtures import MatchingAlgorithm


def test_event(MatchingAlgorithm):
    """Verifies subscription is notified properly"""
    Sub, Event, SubCollection = MatchingAlgorithm

    # initialization, topic=1 msg="simple msg"
    e = Event(1, "simple msg")
    assert e.topic.expose() == 1
    assert e.msg.expose() is "simple msg"

    # initialize with beefier object
    obj = {}
    for i in range(10):
        obj[i] = f"{hash(i)}"
    e = Event(1, obj)
    assert e.topic.expose() == 1
    assert e.msg.expose() is obj


def test_event_serialization(MatchingAlgorithm):
    Sub, Event, SubCollection = MatchingAlgorithm

    e = Event(1, "simple msg")

    # TODO we also need to make sure that the same topic-based classes are
    # imported


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
