#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for FlatInt matching.TopicBased algorithm
"""

from collections import defaultdict
import math
import pytest

from hmap import matching

# create some sort of matching algorithm...

def get_matching_algorithm(FlatNumber):
    return matching.TopicBased(FlatNumber, "PyObject")

def get_callback():
    def cb(topic, msg):
        cb.log.add((topic, msg))
    cb.log = set()
    return cb

def test_subscription(FlatNumber):
    """Verifies subscription is notified properly"""
    A = get_matching_algorithm(FlatNumber)
    S, E, SCollection= (A.Sub, A.Event, A.SubCollection)
    # test callback property
    cb = get_callback()
    s = S(2, cb)
    assert s.callback == cb
    # pass in events
    for i in range(10):
        e = E(i, "msg")
        s.notify(e)
        assert s.callback.log == {(e.topic.expose(), e.msg.expose())}
        s.callback.log = set()

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
      

