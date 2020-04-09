#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from collections import defaultdict
import math

import pytest

from hmap.interfaces import hash_interface, serialize_interface



def test_type_errors(HashableTopicFixture):
    """Confirms exceptions are raised when constructor is misused"""
    for c in HashableTopicFixture.invalid_contents:
        with pytest.raises(Exception):
            instance = HashableTopicFixture.Topic(c)

def test_hashable_topic_interfaces(HashableTopicFixture):
    """verifies all methods function as expected"""
    # list of hashable_instances (some matching some not)
    Topic = HashableTopicFixture.Topic
    contents = HashableTopicFixture.contents
    matches = [(Topic(c), Topic(c)) for c in contents]
    # verify interfaces are happy with topic
    hash_interface.assert_consistency(matches) # IHash
    serialize_interface.assert_consistency(matches) # ISerialize

def test_hashable_topic_content(HashableTopicFixture):
    for c in HashableTopicFixture.contents:
        instance = HashableTopicFixture.Topic(c)
        assert instance.content == c
