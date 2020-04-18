#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import logging

import time

class FHMap(ABC):
    """Base fixture for all hive-map fixtures. Each fixture tests classes and
    their interactions in an inheritable environment.
    """
    logger = logging.getLogger("hmap-interface")
    @abstractmethod
    def instances(self, n):
        """Returns n instances of classes being tested"""
        raise NotImplementedError
    def test(self):
        # TODO go through instances and test them for features(context) 
        # and capabilities(global capabilities)
        tests = set()
        for F in type(self).mro()[::-1]:
            if issubclass(F, FHMap):
                members = [getattr(F, m) for m in dir(F)]
                functions = [m for m in members if callable(m)]
                tests.update([f for f in functions if hasattr(f, "_hmap__test")])
        for t in tests:
            t(self)
def fixture_test(m):
    m._hmap__test = True
    return m

__all__ = ["fixture_test", "FHMap"]
