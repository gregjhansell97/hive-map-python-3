#!/usr/bin/env python
# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod
import time

from hmap.testing import asserts
from hmap.testing.fixtures import FHMap, fixture_test

class FRouter(FHMap):
    @property
    def timeout(self): 
        return 0.5
    @property
    def instances(self):
        return []

    @abstractmethod
    def routers(self, n):
        """n routers instances with no partitions"""
        raise NotImplementedError

    @fixture_test
    def proper_close_operation(self):
        for t in self.instances:
            # for statement checks idempotency
            for i in range(3):
                t.close()
                try:
                    data = t.recv()
                except EOFError:
                    pass
                else:
                    raise AssertionError

