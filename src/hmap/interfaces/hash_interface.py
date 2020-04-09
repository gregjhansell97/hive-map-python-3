#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from abc import ABC, abstractmethod

from hmap.interfaces.equality_interface import (
        IEquality, assert_equality, assert_inequality)

class IHash(IEquality):
    @abstractmethod
    def __hash__(self):
        raise NotImplementedError

def assert_consistency(matches):
    """
    Explain hash consistency

    list of tuples where each tuple set is a group of hash nodes that are
    equal, they are not equal to any nodes outside of tuples
    """
    matches_set = set()
    for instances in matches:
        assert_equality(instances)
        instances_set = set(instances)
        matches_set.update(instances_set)
        assert len(instances_set) == 1
    # adding to a set works
    assert len(matches_set) == len(matches)

    # removing from a set works
    for instances in matches:
        length = len(matches_set)
        # one item should be removed per match tuple
        r_count = 0
        for i in instances:
            try:
                matches_set.remove(i)
                r_count += 1
                assert r_count < 2
            except KeyError:
                pass
        assert length == len(matches_set) + 1

    # check __ne__
    unique_instances = [instances[0] for instances in matches]
    assert_inequality(unique_instances)
