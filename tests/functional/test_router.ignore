#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for Router base class
"""

from collections import defaultdict
import math
import pytest

from hmap import matching

# create some sort of matching algorithm...

def get_router(Router):
    return Router(matching=matching.TopicBased("FlatInt", "PyObject"))

def get_callback():
    def cb(self, topic, msg):
        cb.log.add((topic, msg))
    cb.log = set()

def assert_equal(v1, v2, timeout=1, step=0.1):
    while v1 != v2 and timeout > 0:
        time.sleep(step)
        timeout -= step
    assert v1 == v2


def test_one_subscriber_one_publish(Router):
    """
    Ensures subscription works when a singular event is published
    """
    r = get_router(Router)
    s = r.subscribe(3, get_callback())
    r.publish(3, "m1")
    assert_equal(s.callback.log, {(3, "m1")})

def test_one_subscriber_multiple_publishes(Router):
    """
    Ensures subscription works when multiple events of different topics are 
    published
    """
    r = get_router(Router)
    s = r.subscribe(3, get_callback())
    expected_log = set()
    for i in range(100):
        if i%2 == 0:
            r.publish(3, i)
            expected_log.add((3, i))
    assert_equal(s.callback.log, expected_log)

