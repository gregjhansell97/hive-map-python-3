#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import logging

def test_method(m):
    m._hmap__test = True
    return m

class HMapFixture(ABC):
    """Base fixture for all hive-map fixtures. Each fixture tests classes and
    their interactions in an inheritable environment.
    """
    def __init__(self):
        self.logger = logging.getLogger("hmap-interface")
    @abstractmethod
    def instances(self, n):
        """Returns n instances of classes being tested"""
        raise NotImplementedError

def assert_interface(fixture):
    assert issubclass(type(fixture), HMapFixture)
    # check if it has capabilities
    # test for capability

    # go through hierarchy of fixtures and test functions

    tests = set()
    for F in type(fixture).mro()[::-1]:
        if issubclass(F, HMapFixture):
            members = [getattr(F, m) for m in dir(F)]
            functions = [m for m in members if callable(m)]
            tests.update([f for f in functions if hasattr(f, "_hmap__test")])
    for t in tests:
        t(fixture)

