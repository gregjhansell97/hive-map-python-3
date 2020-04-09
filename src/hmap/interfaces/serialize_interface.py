#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from abc import ABC, abstractmethod

class ISerialize(ABC):
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

def assert_consistency(matches, equal=lambda a, b: a == b):
    """
    List of tuples where each tuple is a group that satisifies equality
    """
    layers = 5
    for instances in matches:
        for i1 in instances:
            Cls = type(i1)
            for i2 in instances:
                # standard
                assert equal(Cls.deserialize(Cls.serialize(i1)), i2)
                # layered
                raw_i1 = Cls.serialize(i1)
                expectedsize = len(raw_i1)
                assert equal(i1.calcsize(), expectedsize)
                # add extra bytes on end of bytestream
                for _ in range(layers):
                    raw_i1 += Cls.serialize(i1)
                i1 = Cls.deserialize(raw_i1)
                assert len(raw_i1) > expectedsize # sanity check
                assert i1.calcsize() == expectedsize
                assert equal(Cls.deserialize(raw_i1), i2)
                assert len(Cls.serialize(i1)) == expectedsize
    # check inequalities too
    instances = [i[0] for i in matches]
    for i1 in instances:
        Cls = type(i1)
        ref_count = 0
        for i2 in instances:
            if i1 is i2:
                assert ref_count < 2
                ref_count += 1
                continue
            assert type(i1) is type(i2), "types must be consistent"
            assert not equal(Cls.deserialize(Cls.serialize(i1)), i2)




