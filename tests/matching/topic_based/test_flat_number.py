#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from collections import defaultdict
import math
import pytest


def test_type_errors(FlatNumber):
    """Confirms exceptions are raised when constructor is misused"""
    with pytest.raises(Exception):
        n1 = FlatNumber("hello world")
    with pytest.raises(Exception):
        # rediculously high number
        n1 = FlatNumber(2 ** (8 * 32))


def test_flat_number_methods(FlatNumber):
    """verifies all methods function as expected"""
    n1 = FlatNumber(10)
    n2 = FlatNumber(10)
    n3 = FlatNumber(3)

    # test __eq__ and __hash__
    assert n1 is not n2
    assert n1 == n2
    assert hash(n1) == hash(n2)
    assert n1 != n3
    assert hash(n1) != hash(n3)

    # test expose
    assert n1.expose() == 10
    assert n3.expose() == 3


def test_serialization(FlatNumber):
    n1 = FlatNumber(3)
    n2 = FlatNumber.deserialize(FlatNumber.serialize(n1))
    assert n1 is not n2
    assert n1 == n2
    assert hash(n1) == hash(n2)
    assert n1.expose() == n2.expose() == 3

    # test with extra bytes at end
    n3 = FlatNumber.deserialize(FlatNumber.serialize(n1) + b"123A")
    assert n1 is not n3
    assert n1 == n3
    assert hash(n1) == hash(n3)
    assert n1.expose() == n3.expose() == 3

    # take through the wringer
    n3 = FlatNumber.deserialize(FlatNumber.serialize(n1) + b"123A")
    for i in range(20):
        bn3 = FlatNumber.serialize(n3)
        assert len(bn3) == n3.calcsize()
        n3 = FlatNumber.deserialize(bn3 + b"123A")
    assert n1 is not n3
    assert n1 == n3
    assert hash(n1) == hash(n3)
    assert n1.expose() == n3.expose() == 3
