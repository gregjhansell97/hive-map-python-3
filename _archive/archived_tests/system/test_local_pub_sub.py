#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests pub-sub network without routers involved, mostly analyzes the interaction
between subscribers and publishers
"""

import pytest

from hmap import Subscriber, Publisher

from tests.functional.test_subscriber import get_callback


def test_one_pub_one_sub_one_connection(Transceiver):
    """
    Get one publisher instance and one subscriber instance and connect them
    over the same topic and confirm that messages get sent 
    """
    TOPIC = 10
    p = Publisher(TOPIC)
    cb = get_callback()
    s = Subscriber(TOPIC, cb)
    Transceiver.connect([p, s])
    p.publish(b"hello")
    assert cb.log == [b"hello"]
    p.publish(b"goodbye")
    assert cb.log == [b"hello", b"goodbye"]


def test_one_pub_one_sub_many_connections(Transceiver):
    """
    Get one publisher instance and one subscriber instance and connect them
    with multiple transceivers and verify that the message only gets delivered
    once... is that a property we want to enforce to some capacity?
    """
    TOPIC = 10
    p = Publisher(TOPIC)
    cb = get_callback()
    s = Subscriber(TOPIC, cb)
    for i in range(10):
        Transceiver.connect([p, s])
    p.publish(b"hello")
    assert cb.log == [b"hello"]
    p.publish(b"goodbye")
    assert cb.log == [b"hello", b"goodbye"]


def test_one_pub_many_sub(Transceiver):
    """
    Get one publisher instance and many subscribers and verify that the 
    messages are published to all subscribers
    """
    TOPIC = 10
    DIFF_TOPIC = 11
    p = Publisher(TOPIC)

    sub_callbacks = [get_callback() for _ in range(10)]
    subs = [Subscriber(TOPIC, cb) for cb in sub_callbacks]

    diff_sub_callbacks = [get_callback() for _ in range(10)]
    diff_subs = [Subscriber(DIFF_TOPIC, cb) for cb in diff_sub_callbacks]
    Transceiver.connect([p] + subs + diff_subs)

    p.publish(b"hello")
    for cb in sub_callbacks:
        assert cb.log == [b"hello"]
    for cb in diff_sub_callbacks:
        assert cb.log == []

    p.publish(b"goodbye")
    for cb in sub_callbacks:
        assert cb.log == [b"hello", b"goodbye"]
    for cb in diff_sub_callbacks:
        assert cb.log == []


def test_many_pub_one_sub(Transceiver):
    """
    Get many publisher instances and many subscribers and verify that the 
    messages are published to the subscriber
    """
    TOPIC = 10
    DIFF_TOPIC = 11
    pubs = [Publisher(TOPIC) for _ in range(10)]
    diff_pubs = [Publisher(DIFF_TOPIC) for _ in range(10)]

    cb = get_callback()
    sub = Subscriber(TOPIC, cb)

    Transceiver.connect([sub] + pubs + diff_pubs)

    expected_log = []
    pubs[0].publish(b"hello")
    expected_log.append(b"hello")
    assert cb.log == expected_log

    for p in diff_pubs:
        p.publish(b"kaput")
    assert cb.log == [b"hello"]

    for p in pubs:
        p.publish(b"works")
        expected_log.append(b"works")
    assert cb.log == expected_log


def test_many_pub_many_sub(Transceiver):
    """
    Get many publisher instances and many subscribers and verify that the 
    messages are published to all subscribers
    """
    TOPIC = 10
    DIFF_TOPIC = 11
    pubs = [Publisher(TOPIC) for _ in range(10)]
    diff_pubs = [Publisher(DIFF_TOPIC) for _ in range(10)]

    sub_callbacks = [get_callback() for _ in range(10)]
    subs = [Subscriber(TOPIC, cb) for cb in sub_callbacks]

    diff_sub_callbacks = [get_callback() for _ in range(10)]
    diff_subs = [Subscriber(DIFF_TOPIC, cb) for cb in diff_sub_callbacks]
    Transceiver.connect(pubs + diff_pubs + subs + diff_subs)

    expected_log = []
    expected_diff_log = []

    pubs[0].publish(b"sign")
    expected_log.append(b"sign")
    for cb in sub_callbacks:
        assert cb.log == expected_log
    for cb in diff_sub_callbacks:
        assert cb.log == expected_diff_log

    for p in pubs:
        p.publish(b"open eyes")
        expected_log.append(b"open eyes")
    for p in diff_pubs:
        p.publish(b"belong")
        expected_diff_log.append(b"belong")
    for cb in sub_callbacks:
        assert cb.log == expected_log
    for cb in diff_sub_callbacks:
        assert cb.log == expected_diff_log
