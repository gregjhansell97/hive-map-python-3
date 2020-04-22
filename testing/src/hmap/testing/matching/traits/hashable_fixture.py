#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from hmap.testing import asserts
from hmap.testing.fixtures import FHMap, fixture_test
from hmap.interface.matching.traits import Hashable


class FHashable(FHMap):

    @property
    @abstractmethod
    def hash_instances(self):
        raise NotImplementedError
    @fixture_test
    def is_equal_noequal_properties(self):
        instances = self.hash_instances + self.hash_instances
        for i in instances:
            for j in instances:
                if i is j:
                    asserts.equal(hash(i), hash(j))
                if i == j:
                    asserts.equal(hash(i), hash(j))
