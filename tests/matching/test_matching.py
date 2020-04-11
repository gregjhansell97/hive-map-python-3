#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from collections import defaultdict
import math

import pytest

from hmap.interfaces import serialize_interface


def test_matching_component_uniqueness(FMatchingComponent):
    instances = FMatchingComponent.instances(5)
    serialize = FMatchingComponent.InstanceType.serialize
    deserialize = FMatchingComponent.InstanceType.deserialize
    equal = FMatchingComponent.equal
    # although equal is true does not equal its copied counter part
    for i in instances:
        assert i != deserialize(serialize(i))

def test_basic_sub_collection(FSub):
    Sub = FSub.InstanceType
    subs_count = 10 
    subs = FSub.instances(subs_count)
    assert subs_count == len(subs)

    assert len(set(subs)) == subs_count, "subs must be unique"
    subs1 = subs[:subs_count//2]
    subs2 = subs[subs_count//2:]
    col1 = Sub.Collection()
    col2 = Sub.Collection()
    assert col1 is not col2
    assert col1 != col2
    for s in subs1:
        col1.add(s)
    assert set(subs1) == {s for s in col1}
    assert len(subs1) == len([s for s in col1]) # no duplicates
    col1.remove(subs1[0])
    with pytest.raises(KeyError):
        col1.remove(subs1[0])
    with pytest.raises(KeyError):
        col1.remove(subs2[0])
    assert set(subs1[1:]) == {s for s in col1}, "removed right sub"
    col2.add(subs1[0])
    col2.extend(col1)
    assert col2 != col1
    assert set(subs1[1:]) == {s for s in col1}, "col1 doesn't change"
    assert set(subs1) == {s for s in col2}, "col2 is a copy with first sub"
    for s in subs2:
        col2.add(s)
    assert set(subs1[1:]) == {s for s in col1}, "col1 doesn't change"
    assert set(subs) == {s for s in col2}, "col2 is a copy with first sub"
    col2.extend(col1)
    assert len(subs) == len([s for s in col2]), "no duplicates"

    


    
