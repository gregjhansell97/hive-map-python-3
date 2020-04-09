#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for hive_map.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

import pytest

from hmap.matching.topic_based.msg_types import PyObj
from hmap.matching.topic_based.topic_types import (
        FlatInt, FlatByte, FlatUInt, FlatUByte)

def pytest_generate_tests(metafunc):
    """
    Customize test functions however needed
    """
    if "Impl" in metafunc.fixturenames:
        # parameterize FlatNumber classes
        impl_fixtures = [
                FlatNumberImpl, 
                PyObjImpl
        ]
        metafunc.parametrize("Impl", impl_fixtures)

def FlatNumberImpl():
    def eq(n1, n2):
        return type(n1) is type(n2) and n1 == n2
    instances = []
    # FlatInt
    content = [
        -(2**32)//2,
        -42,
        0,
        32,
        (2**32)//2 - 1
    ]
    instances += [FlatInt(c) for c in content]
    # FlatUInt
    content = [
        0,
        32, 
        2**(32) - 1
    ]
    instances += [FlatUInt(c) for c in content]
    # FlatByte
    content = [
        -128,
        -42,
        0,
        32,
        127
    ]
    instances += [FlatByte(c) for c in content]
    # FlatUByte
    content = [
        0,
        32,
        255,
    ]
    instances += [FlatUByte(c) for c in content]
    return (instances, eq)

def PyObjImpl():
    def eq(m1, m2):
        return type(m1) is type(m2) and m1.content == m2.content
    instances = [
            PyObj((1, 2, "tuple", {"A": 1})),
            PyObj(()),
            PyObj(None)]
    return (instances, eq)
