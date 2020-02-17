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


def parametrize_test_one_location_one_destination_direct_connection(
        reliability=1,
        destination_reliability=(1, 1),
        iterations=100
    ):
    """
    Confirms the basic expectation that publishing a message

    Args:
        reliability: simulated connection reliability between the location
            and destination
        destination_reliability: expected destination reliability after running
            communication channel
    """
    l = Location(1)
    d = Destination(1)
    cb = get_callback()
    l.subscribe(cb)

    LocalSocket.connect(l, d, reliability=reliability)

    # for loop ensures that message dependibility doesn't decrease over time
    for i in range(iterations):
        msgs = {b"hello world", b"127", b"my name is greg"}
        for m in msgs:
            d.publish(m)
        if reliability >= 1:
            assert cb.log == msgs, "sent messages should be received"
        else:
            assert cb.log | msgs == msgs, "no weird messages"
                    
        cb.log = set()
    assert d.reliability >= destination_reliability[0]
    assert d.reliability <= destination_reliability[1]
    assert d.distance == 1

def test_one_location_one_destination_direct_connection():
    # basic network, perfect connection
    parametrize_test_one_location_one_destination_direct_connection(
            reliability=1,
            destination_reliability=(1, 1),
            iterations=100)

    # when the network is overly-reliabile (same message sent more than once)
    #parametrize_test_one_location_one_destination_direct_connection(
    #        reliability=3,
    #        destination_reliability=(1, 1))

    # when network drops some messages
    #parametrize_test_one_location_one_destination_direct_connection(
    #        reliability=0.5,
    #        destination_reliability=(1, 1),
    #        iterations=100)
    #parametrize_test_one_location_one_destination_direct_connection(
    #    reliability=0.5,
    #    expected_reliability=(0.3, 0.7))

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
    print(d1.reliability)
    print(d2.reliability)
    print(d3.reliability)
    print(d4._distances_table)
    print(d5.reliability)
    assert d1.distance == 1
    assert d2.distance == 1
    assert d3.distance == 2
    assert d4.distance == 2
    assert d5.distance == 3
