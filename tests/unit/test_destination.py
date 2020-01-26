#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import pytest

from hmap.loc import Destination

from tests.local_socket import LocalSocket


def get_destinations(size, reliability=0.9):
    return [Destination(t, reliability=reliability) for t in range(size)]


def test_initialization():
    """
    Verify destination starts up with a unique id describing destination
    """
    d = Destination(1)
    assert d.target == 1

def test_initialization_error():
    """
    Verify that value error is raised when input parameters do not make sense
    """
    try:
        # reliability must be between 0 and 1
        d = Destination(1, reliability=1.1)
    except ValueError:
        assert True
    else:
        assert False

    try:
        # learning rate must be between 0 and 1
        d = Destination(1, learning_rate=-0.5)
    except ValueError:
        assert True
    else:
        assert False


def test_use_socket_one_destination():
    """
    Verify that a provided socket can be used by a destination
    """
    d = Destination(1)
    s = LocalSocket.get_sockets(1)[0]
    d.use(s)
    try:
        d.use(s)
    except ValueError:
        assert True
    else:
        assert False


def test_use_socket_multiple_destination():
    """
    Verify that one socket can be used for multiple destinations
    """
    destinations = get_destinations(10)
    s = LocalSocket.get_sockets(1)[0]
    for d in destinations:
        d.use(s)


def test_use_socket_multiple_times_on_destination():
    """
    Verify that one socket used more than once on a destination raises an error
    """
    d = Destination(1)
    s = LocalSocket.get_sockets(1)[0]
    d.use(s)
    try:
        d.use(s)
    except ValueError:
        assert True
    else:
        assert False


def test_use_sockets_one_destination():
    """
    Verify multiple sockets can be used by one destination
    """
    sockets = LocalSocket.get_sockets(10)
    d = Destination(1)
    for s in sockets:
        d.use(s)


def test_use_sockets_multiple_destination_with_overlap():
    """
    Verify multiple sockets can be used by multiple destinations
    """
    destinations = get_destinations(10)
    sockets = LocalSocket.get_sockets(10)
    for d in destinations:
        for s in sockets:
            d.use(s)


def test_update_distance():
    """
    Verify that the internal methods: _decrement_reliability and
    _increment_reliability change the distance and reliability as expected. If
    the system becomes less reliabilty the node should increase its distance
    and if the system becomes reliabile at a certain distance it should stay
    at that distance
    """
    d = Destination(1)
    distance = d.distance
    assert d.distance == math.inf
    assert d.reliability == 0.0
    for i in range(100):
        r = d.reliability
        d._decrement_reliability(3)
        d._increment_reliability(3, 1)
        assert d.reliability >= r
    assert d.distance == 3
    for i in range(100):
        r = d.reliability
        d._decrement_reliability(3)
        assert d.reliability <= r
    assert d.reliability == 0.0
    assert d.distance == math.inf
    for i in range(100):
        d._decrement_reliability(3)
        d._increment_reliability(3, 0.5)
    assert d.distance == math.inf
    assert d.reliability > 0.4
    for i in range(100):
        d._decrement_reliability(2)
        d._increment_reliability(2, 0.85)
    assert d.distance == 3
    assert d.reliability > 0.9
    for i in range(100):
        d._decrement_reliability(4)
        d._increment_reliability(4, 0)
        d._increment_reliability(3, 0.5)
        d._increment_reliability(2, 0.85)
    assert d.distance == 3
