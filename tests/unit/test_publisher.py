#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for LocalSocket; the main target of these tests is AbstractSocket
"""

from collections import defaultdict
import pytest

from hmap import Publisher

from tests.local_transceiver import LocalTransceiver

def test_initialization():
    p = Publisher(10)

def test_use_transceiver():
    # set up publisher
    p = Publisher(10)
    t = LocalTransceiver()
    p.use(t)

def test_use_multiple_transceivers():
    # set up publisher
    p = Publisher(5)
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        p.use(t)

def test_publish_no_transceiver():
    p = Publisher(5)
    p.publish(b"hello world")

def test_publish_one_transceiver():
    p = Publisher(5)
    t = LocalTransceiver()
    p.use(t)
    p.publish(b"hello world")

def test_publish_many_transceivers():
    p = Publisher(5)
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    p.publish(b"goodbye yellow brick road")

def test_many_publish_many_transceivers():
    p = Publisher(5)
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    p.publish(b"goodbye yellow brick road")

