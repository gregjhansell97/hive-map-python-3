#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from hmap import Location, Destination
from tests.local_socket import LocalSocket

def get_callback():
    def cb(msg):
        cb.log.append(msg)
    cb.log = []
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
        msgs = [b"hello world", b"127", b"my name is greg"]
        for m in msgs:
            d.publish(m)
        assert cb.log == msgs, "sent messages should be received"
        cb.log = []
    assert d.distance == 1
    print(d.reliability)
    assert d.reliability == 1.0

