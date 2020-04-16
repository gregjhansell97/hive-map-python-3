#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from hmap.interface.testing import interface_test
from hmap.interface.matching.topic_based.testing import TopicBasedMatchingFixture
from hmap.std.matching.topic_based import Matcher
from hmap.std.matching.topic_based.topic_types import FlatInt
from hmap.std.matching.topic_based.msg_types import PyObj


class FlatIntPyObjMatchingFixture(TopicBasedMatchingFixture):
    def matchers(self, n):
        return [Matcher("FlatInt", "PyObj") for _ in range(n)]
    def topics(self, n):
        return [FlatInt(i) for i in range(n)]
    def messages(self, n):
        return [PyObj(f"i") for i in range(n)]

def test_hello_world(caplog):
    caplog.set_level(logging.DEBUG)
    interface_test(FlatIntPyObjMatchingFixture())
