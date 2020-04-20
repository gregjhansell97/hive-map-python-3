#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pytest
import uuid

import time

#interface
from hmap.testing.routing.fixtures import FRouter
# standard library
from hmap.std.routing import LocalRouter
from hmap.std.matching import topic_based

def test_local_router():
    r = LocalRouter(matcher=topic_based.Matcher("FlatInt", "PyObj"))
    def cb(topic, msg):
        cb.log.append((topic, msg))
    cb.log = []
    r.subscribe(1, cb)
    r.publish(1, "hello world")
    assert cb.log == [(1, "hello world")]

