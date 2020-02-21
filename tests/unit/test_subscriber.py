#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for LocalSocket; the main target of these tests is AbstractSocket
"""

from collections import defaultdict
import pytest

from hmap import Subscriber

from tests.local_transceiver import LocalTransceiver

def get_callback():
    """
    Creates a callback instance that tracks invocations. This function was
    created because a lot of tests create a callback!
    
    Returns (lambda t, d): callback that takes in a transceiver and data as
        arguments
    """
    def cb(data: bytes):
        # callbacks for transceivers expects a transceiver instance and 
        # raw-bytes being received
        cb.log.append(data)
    cb.log = [] # log tracks the data received and by which transceiver
    return cb

def test_initialization():
    cb = get_callback()
    s = Subscriber(10, cb)

def test_use_transceiver():
    cb = get_callback()
    # set up publisher
    s = Subscriber(10, cb)
    t = LocalTransceiver()
    s.use(t)

def test_use_multiple_transceivers():
    # set up publisher
    cb = get_callback()
    s = Subscriber(5, cb)
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        s.use(t)

