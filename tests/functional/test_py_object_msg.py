#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for FlatInt matching.TopicBased algorithm
"""

from collections import defaultdict
import math
import pytest

from hmap.matching.topic_based.msg_types import PyObj

def test_py_obj_methods():
    """Verifies all methods function as expected"""
    obj1 = (1, 2, "does this work", {"As": 1})
    obj2 = (1, 2, "different", {"As": 1})
    m1 = PyObj(obj1)
    m1_copy = PyObj(obj1)
    m2 = PyObj(obj2)

    assert m1 != m1_copy
    assert m1.expose() == obj1 == m1_copy.expose()
    assert m1 != m2
    assert m1.expose() != m2.expose()
    


def test_serialization():
    obj1 = (1, 2, "does this work", {"As": 1})
    m1 = PyObj(obj1)

    ms = PyObj.deserialize(PyObj.serialize(m1))
    # try with bytes on end
    ms = PyObj.deserialize(PyObj.serialize(m1) + b"extra bytes")
    assert ms != m1
    assert ms.expose() == m1.expose() == obj1

    # multiple layers of serialization and deserialization
    for i in range(20):
        bms = PyObj.serialize(ms)
        assert len(bms) == ms.calcsize()
        ms = PyObj.deserialize(PyObj.serialize(ms))
    assert ms != m1
    assert ms.expose() == m1.expose() == obj1

