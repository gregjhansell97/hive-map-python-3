#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from hmap import Location, Destination
from tests.local_socket import LocalSocket


def get_callback():
    def cb(msg):
        cb.log.add(msg)

    cb.log = set()
    return cb


def test_one_location_one_destination_direct_connection():
    """
    Confirms the basic expectation that publishing a message
    """
    l = Location(1)
    d = Destination(1)
    cb = get_callback()
    l.subscribe(cb)

    sockets = LocalSocket.get_sockets(2)
    l.use(sockets[0])
    d.use(sockets[1])

    # for loop ensures that message dependibility doesn't decrease over time
    for i in range(100):
        msgs = {b"hello world", b"127", b"my name is greg"}
        for m in msgs:
            d.publish(m)
        assert cb.log == msgs, "sent messages should be received"
        cb.log = set()
    assert d.distance == 1
    assert d.reliability == 1.0

def test_one_location_two_destinations_indirect_connection():
    """
    Confirms that destiantions work together in the most basic capacity. One
    of the destinations will have to send its message through another
    destination
    """
    l = Location(1)
    d1 = Destination(1)
    d2 = Destination(1)
    cb = get_callback()
    l.subscribe(cb)

    LocalSocket.connect(l, d1)
    LocalSocket.connect(d1, d2)

    msgs = {b"hello world", b"127", b"my name is greg"}
    for i in range(100):
        for m in msgs:
            d1.publish(m)
        assert cb.log == msgs, "sent messages should be received"
        cb.log = set() # clears the log
    assert d1.distance == 1
    for i in range(100):
        for m in msgs:
            d2.publish(m)
        assert cb.log == msgs, "sent messages should be received"
        cb.log = set()
    assert d2.distance == 2

def test_one_location_five_interconnected_destinations():
    """
    Confirms that destinations work toegther in a more complicated capacity,
    destinations will have to send messages through another destination. The
    end node may receive more than one message
    l----d1--------d3------d5
       |        /  |
       ---d2-------d4
    """
    l = Location(1)
    cb = get_callback()
    l.subscribe(cb)

    d1 = Destination(1)
    d2 = Destination(1)
    d3 = Destination(1)
    d4 = Destination(1)
    d5 = Destination(1)

    LocalSocket.connect(l, d1)
    LocalSocket.connect(l, d2)
    LocalSocket.connect(d1, d3)
    LocalSocket.connect(d2, d3)
    LocalSocket.connect(d2, d4)
    LocalSocket.connect(d3, d4)
    LocalSocket.connect(d3, d5)

    # need to start with closest ones
    def publish_messages(d):
        for i in range(100):
            msgs = {b"hello world", b"4", b"gerg waz here"}
            for m in msgs:
                d.publish(m)
            assert cb.log == msgs, "sent messages should be received"
            cb.log = set()
    publish_messages(d1)
    publish_messages(d2)
    publish_messages(d3)
    publish_messages(d4)
    publish_messages(d5)
    assert d1.distance == 1
    assert d2.distance == 1
    assert d3.distance == 2
    assert d4.distance == 2
    assert d5.distance == 3
