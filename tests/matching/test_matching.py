#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from collections import defaultdict
import math

import pytest

from hmap.interfaces import serialize_interface


def test_matching_component_uniqueness(FMatchingComponent):
    instances = FMatchingComponent.instances()
    serialize = FMatchingComponent.InstanceType.serialize
    deserialize = FMatchingComponent.InstanceType.deserialize
    equal = FMatchingComponent.equal
    # although equal is true does not equal its copied counter part
    for i in instances:
        assert i != deserialize(serialize(i))
