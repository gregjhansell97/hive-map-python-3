#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for Router. Does not test actual receiving of messages, that is
in the system tests
"""

from collections import defaultdict
import pytest

from hmap import Router


def test_initialization():
    """
    Verifies router can take in a topic and callback without crashing
    """
    r = Router()


def test_use_transceiver(Transceiver):
    """
    Verifies subscriber can use a transceiver without crashing
    """
    r = Router()
    t = Transceiver()
    r.use(t)


def test_use_multiple_transceivers(Transceiver):
    """
    Verifies subscriber can use multiple tranceivers without crashing
    """
    # set up publisher
    r = Router()
    ts = [Transceiver() for _ in range(10)]
    for t in ts:
        r.use(t)
