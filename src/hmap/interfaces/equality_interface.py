#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from abc import ABC, abstractmethod

class IEquality(ABC):
    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError
    def __ne__(self, other):
        return not (self == other)

def assert_equality(instances):
    """
    Each argument is an instance that should be equal to every other instance
    provided
    """
    for i in instances:
        for j in instances:
            assert i == j
            assert j == i
            assert not i != j
            assert not j != i

def assert_inequality(instances):
    """
    Each argument is an instance that should be not equal to every other 
    instance provided
    """
    for i in instances:
        ref_count = 0
        for j in instances:
            if i is j:
                ref_count += 1
                assert ref_count < 2
            else:
                assert i != j
                assert j != i
                assert not i == j
                assert not j == i
        assert ref_count == 1
