#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for Publisher
"""

from collections import defaultdict
import pytest

from hmap import Publisher


def test_initialization():
    """
    Verify publisher can take in a topic and not crash
    """
    p = Publisher(10)


def test_use_transceiver(Transceiver):
    """
    Verify publisher can use a transceiver object
    """
    # set up publisher
    p = Publisher(10)
    t = Transceiver()
    p.use(t)


def test_use_multiple_transceivers(Transceiver):
    """
    Verify publisher can use multiple transceivers
    """
    # set up publisher
    p = Publisher(5)
    ts = [Transceiver() for _ in range(10)]
    for t in ts:
        p.use(t)


def test_publish_no_transceiver():
    """
    Verify publisher can publish even with no means of transceiver. May want to
    consider raising an error if publish is called with no tranceiver...
    """
    p = Publisher(5)
    p.publish(b"hello world")


def test_publish_one_transceiver(Transceiver):
    """
    Verify publish works with when using one tranceiver
    """
    p = Publisher(5)
    t = Transceiver()
    p.use(t)
    p.publish(b"hello world")


def test_publish_many_transceivers(Transceiver):
    """
    Verify publish works with when using multiple tranceivers
    """
    p = Publisher(5)
    ts = [Transceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    p.publish(b"goodbye yellow brick road")


def test_many_publish_many_transceivers(Transceiver):
    """
    Verify publish works many times with when using multiple tranceivers
    """
    p = Publisher(5)
    ts = [Transceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    for i in range(10):
        p.publish(b"goodbye yellow brick road")
