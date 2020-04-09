#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from collections import defaultdict
import math

import pytest

from hmap.interfaces import serialize_interface


def test_type_errors(MsgFixture):
    """Confirms exceptions are raised when constructor is misused"""
    for c in MsgFixture.invalid_contents:
        with pytest.raises(Exception):
            instance = MsgFixture.Topic(c)

def test_hashable_topic_interfaces(MsgFixture):
    """verifies all methods function as expected"""
    # list of hashable_instances (some matching some not)
    Msg = MsgFixture.Msg
    contents = MsgFixture.contents
    matches = [(Msg(c), Msg(c)) for c in contents]
    # verify interfaces are happy with topic
    serialize_interface.assert_consistency(matches) # ISerialize

def test_hashable_topic_content(MsgFixture):
    for c in MsgFixture.contents:
        instance = MsgFixture.Msg(c)
        assert instance.content == c


