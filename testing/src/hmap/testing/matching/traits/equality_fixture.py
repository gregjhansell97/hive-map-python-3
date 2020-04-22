#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from hmap.testing import asserts
from hmap.testing.fixtures import FHMap, fixture_test
from hmap.interface.matching.traits import Equality


class FEquality(FHMap):
    @property
    @abstractmethod
    def equality_instances(self):
        raise NotImplementedError
    @fixture_test
    def is_equal_noequal_properties(self):
        instances = self.instances + self.instances
        for i in instances:
            asserts.true(issubclass(type(i), Equality))
            for j in instances:
                if i is j:
                    asserts.true(j is i)
                    asserts.equal(i, j)
                    asserts.equal(j, i)
                if i == j:
                    asserts.equal(j, i)
                    asserts.false(j != i)
                    asserts.false(i != j)
                if i != j:
                    asserts.not_equal(j, i)
                    asserts.false(i == j)
                    asserts.false(i == j)
                    asserts.false(i is j)
                    asserts.false(j is i)



