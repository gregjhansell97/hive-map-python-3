#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from abc import ABC, abstractmethod

from hmap.interfaces.equality_interface import (
        IEquality, assert_equality, assert_inequality)

class ISerialize(IEquality):
    @abstractmethod
    def calcsize(self):
        raise NotImplementedError
    @classmethod
    @abstractmethod
    def serialize(cls, instance):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def deserialize(cls, raw_data, lazy=False):
        raise NotImplementedError

def assert_consistency(matches):
    """
    List of tuples where each tuple is a group that satisifies equality
    """
    layers = 5
    for instances in matches:
        assert_equality(instances)
        for i1 in instances:
            Cls = type(i1)
            for i2 in instances:
                # standard
                assert Cls.deserialize(Cls.serialize(i1)) == i2
                # layered
                raw_i1 = Cls.serialize(i1)
                expectedsize = len(raw_i1)
                assert i1.calcsize() == expectedsize
                # add extra bytes on end of bytestream
                for _ in range(layers):
                    raw_i1 += Cls.serialize(i1)
                i1 = Cls.deserialize(raw_i1)
                assert len(raw_i1) > expectedsize # sanity check
                assert i1.calcsize() == expectedsize
                assert Cls.deserialize(raw_i1) == i2
                assert len(Cls.serialize(i1)) == expectedsize
    # check inequalities too
    instances = [i[0] for i in matches]
    assert_inequality(instances)
    for i1 in instances:
        Cls = type(i1)
        ref_count = 0
        for i2 in instances:
            if i1 is i2:
                assert ref_count < 2
                ref_count += 1
                continue
            assert type(i1) is type(i2), "types must be consistent"
            assert Cls.deserialize(Cls.serialize(i1)) != i2




