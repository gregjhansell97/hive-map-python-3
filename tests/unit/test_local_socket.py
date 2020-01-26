#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for LocalSocket; the main target of these tests is AbstractSocket
"""

from collections import defaultdict
import pytest

from tests.local_socket import LocalSocket


def test_initialization():
    """
    Ensures that local sockets can be created
    """
    sockets = LocalSocket.get_sockets(10)


def test_subscribe():
    """
    Ensures that _subscribe method of hmap.sockets.AbstractSocket works in the
    most basic capacity
    """
    s = LocalSocket.get_sockets(1)[0]
    s._subscribe(2, None)

def test_subscribe_value_error():
    """
    Ensures that _subscribe method of hmap.sockets.AbstractSocket raises a value
    error when more than one subscriber is being added for one id...
    """
    s = LocalSocket.get_sockets(1)[0]
    s._subscribe(2, None)
    try:
        s._subscribe(2, None)
    except ValueError:
        assert True
    else:
        assert False

def test_publish():
    """
    Ensures that _publish method of hmap.sockets.AbstractSocket works in the
    most basic capacity
    """
    s = LocalSocket.get_sockets(1)[0]
    s._publish(2, b"message in a bottle")


def get_callback():
    """
    Creates a callback instance that tracks a lof of all invocations. This
    function was created because a lot of tests create a callback

    Returns:
        (lambda s,t,d): callback used for subscriptions in tests. All callbacks
            have an attribute called log which shows the list of all invocations
            of the method.
    """

    def cb(socket: LocalSocket, topic: int, data: bytes):
        cb.log.append((socket, topic, data))

    cb.log = []
    return cb

def test_publish_subscribe_2_socket_network():
    """
    Create two sockets and have one publish data and the other receive that
    data
    """
    cb = get_callback()

    sockets = LocalSocket.get_sockets(2)
    sockets[1]._subscribe(2, cb)
    p_count = 10
    for i in range(p_count):
        sockets[0]._publish(2, b"hello world")
    assert cb.log == [(sockets[1], 2, b"hello world")] * 10


def test_publish_subscribe_multiple_socket_network():
    """
    Creates several sockets on the same network and verifies that publishes make
    it to all sockets
    """
    cb = get_callback()

    sockets = LocalSocket.get_sockets(10)
    # each socket has their own callback
    callbacks = [get_callback() for s in sockets]

    # subscribe all sockets to their corresponding callbacks
    for s, cb, i in zip(sockets, callbacks, range(len(sockets))):
        s._subscribe(i, cb)

    sockets[1]._publish(11, b"hello world")
    for cb in callbacks:
        assert cb.log == []

    sockets[1]._publish(2, b"hello world")
    for i, cb in zip(range(len(callbacks)), callbacks):
        if i == 2:
            assert cb.log == [(sockets[2], 2, b"hello world")]
        else:
            assert cb.log == []

    sockets[1]._publish(5, b"hello world")
    sockets[1]._publish(5, b"hello world")
    assert callbacks[5].log == 2 * [(sockets[5], 5, b"hello world")]

    sockets[5]._publish(8, b"hello world")
    assert callbacks[8].log == [(sockets[8], 8, b"hello world")]

    sockets[4]._publish(4, b"hello world")
    assert callbacks[4].log == []  # does not look at local subscribers
