#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pytest

from hmap.interface.testing import assert_interface
from hmap.interface.matching.topic_based.testing import TopicBasedMatchingFixture
from hmap.std.matching.topic_based import Matcher
from hmap.std.matching.topic_based.msg_types import PyObj




class FFlatNumber(TopicBasedMatchingFixture):
    def __init__(self, topic_type, max_t, min_t):
        super().__init__()
        self.max_t = max_t
        self.min_t = min_t
        self.topic_type = topic_type
    def matchers(self, n):
        return [Matcher(self.topic_type, "PyObj") for _ in range(n)]
    def topics(self, n):
        matcher = self.matcher
        ts = []
        for offset in range((n//2) + 1):
            ts += [
                    matcher.Event.Topic(self.max_t - offset), 
                    matcher.Event.Topic(self.min_t + offset)]
        return ts[:n]
    def msgs(self, n):
        return [PyObj(f"i") for i in range(n)]

@pytest.mark.parametrize("topic_type,min_t,max_t", [
        ("FlatByte", -128, 127),
        ("FlatUByte", 0, 255),
        ("FlatInt", -2**32//2, (2**32)//2 - 1),
        ("FlatUInt", 0, 2**32 - 1)])
def test_flat_number(topic_type, max_t, min_t):
    fn_fixture = FFlatNumber(topic_type, max_t, min_t)
    Topic = fn_fixture.matcher.Event.Topic
    assert_interface(fn_fixture)
    for tcontent in range(fn_fixture.min_t, fn_fixture.min_t + 10):
        # TODO expose Topic & Msg to matcher?
        assert fn_fixture.matcher.Event.Topic(tcontent).content == tcontent

