#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for LocalSocket; the main target of these tests is AbstractSocket
"""

from collections import defaultdict
import pytest

from hmap import Publisher


def test_initialization():
    p = Publisher(10)


def test_use_transceiver(Transceiver):
    # set up publisher
    p = Publisher(10)
    t = Transceiver()
    p.use(t)


def test_use_multiple_transceivers(Transceiver):
    # set up publisher
    p = Publisher(5)
    ts = [Transceiver() for _ in range(10)]
    for t in ts:
        p.use(t)


def test_publish_no_transceiver():
    p = Publisher(5)
    p.publish(b"hello world")


def test_publish_one_transceiver(Transceiver):
    p = Publisher(5)
    t = Transceiver()
    p.use(t)
    p.publish(b"hello world")


def test_publish_many_transceivers(Transceiver):
    p = Publisher(5)
    ts = [Transceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    p.publish(b"goodbye yellow brick road")


def test_many_publish_many_transceivers(Transceiver):
    p = Publisher(5)
    ts = [Transceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    p.publish(b"goodbye yellow brick road")
