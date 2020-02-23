#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for LocalSocket; the main target of these tests is AbstractSocket
"""

from collections import defaultdict
import pytest

def get_callback():
    """
    Creates a callback instance that tracks invocations. This function was
    created because a lot of tests create a callback!
    
    Returns (lambda t, d): callback that takes in a transceiver and data as
        arguments
    """
    def cb(t, data: bytes):
        # callbacks for transceivers expects a transceiver instance and 
        # raw-bytes being received
        cb.log.append((t, data))
    cb.log = [] # log tracks the data received and by which transceiver
    return cb


def test_initialization(Transceiver):
    """
    Ensures that local transceivers can be created
    """
    connections = Transceiver.get_connections(10)

def test_subscribe(Transceiver):
    """
    Ensures that _subscribe method of hmap.Transceiver works as expected
    """
    t = Transceiver.get_connections(10)[0]
    t._subscribe(None)

def test_publish_subscribe_2_socket_network(Transceiver):
    """
    Create two transceivers and have one transmit data and the other receive 
    that data
    """
    cb = get_callback()

    connections = Transceiver.get_connections(2)
    connections[1]._subscribe(cb)
    p_count = 10
    # go through and publish data
    for i in range(p_count):
        connections[0].transmit(b"hello world")
    assert cb.log == [(connections[1], b"hello world")] * 10

def test_publish_subscribe_multiple_socket_network(Transceiver):
    """
    Creates several transceivers on the same network and verifies that successful
    transmissions
    """
    cb = get_callback()

    connections = Transceiver.get_connections(10)
    # each socket has their own callback
    callbacks = [get_callback() for _ in connections]

    # subscribe all sockets to their corresponding callbacks
    for c, cb, i in zip(connections, callbacks, range(len(connections))):
        c._subscribe(cb)

    connections[1].transmit(b"hello world")
    for c, cb in zip(connections, callbacks):
        if c == connections[1]:
            assert cb.log == []
            cb.log.append((c, b"hello world")) # consistent throughout now
        # useful for checking stuff later
        assert cb.log == [(c, b"hello world")]

    connections[5].transmit(b"lucky 5")
    for c, cb in zip(connections, callbacks):
        if c == connections[5]:
            assert cb.log == [(c, b"hello world")]
            cb.log.append((c, b"lucky 5"))
        assert cb.log == [(c, b"hello world"), (c, b"lucky 5")]
