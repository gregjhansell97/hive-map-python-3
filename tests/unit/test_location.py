#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from hmap.loc import Location

from tests.local_socket import LocalSocket


def get_locations(size):
    return [Location(i) for i in range(size)]


def test_initialization():
    """
    Verify location starts up with a unique id describing location
    """
    l = Location(1)

    def callback(msg):
        pass

    l.subscribe(callback)


def test_use_socket_one_location():
    """
    Verify that a provided socket can be used by a location
    """
    l = Location(1)
    s = LocalSocket.get_sockets(1)[0]
    l.use(s)


def test_use_socket_multiple_locations():
    """
    Verify that one socket can be used for multiple locations
    """
    locations = get_locations(10)
    s = LocalSocket.get_sockets(1)[0]
    for l in locations:
        l.use(s)


def test_use_socket_multiple_times_on_location():
    """
    Verify that one socket used more than once on a location raises an error
    """
    l = Location(1)
    s = LocalSocket.get_sockets(1)[0]
    l.use(s)
    try:
        l.use(s)
    except ValueError:
        assert True
    else:
        assert False


def test_use_sockets_one_location():
    """
    Verify multiple sockets can be used by one location
    """
    sockets = LocalSocket.get_sockets(10)
    l = Location(1)
    for s in sockets:
        l.use(s)


def test_use_sockets_multiple_location_with_overlap():
    """
    Verify multiple sockets can be used by multiple locations
    """
    locations = get_locations(10)
    sockets = LocalSocket.get_sockets(10)
    for l in locations:
        for s in sockets:
            l.use(s)
