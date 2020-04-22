#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from hmap.testing import asserts
from hmap.testing.fixtures import FHMap, fixture_test
from hmap.interface.matching.traits import Serializable


class FSerializable(FHMap):
    @property
    @abstractmethod
    def serializable_instances(self):
        raise NotImplementedError
    @fixture_test
    def serializable_sub_class(self):
        for i in self.serializable_instances:
            asserts.true(issubclass(type(i), Serializable))
    @fixture_test
    def is_equal_noequal_properties(self):
        instances = self.serializable_instances
        layers = 5
        for i in instances:
            serialize = type(i).serialize
            deserialize = type(i).deserialize
            for _ in range(layers):
                raw_i = serialize(i)
                asserts.equal(len(raw_i), i.calcsize())
                asserts.true(i.serially_equal(deserialize(raw_i)))
                raw_i += raw_i + b"DEADBEEF"
                asserts.true(i.serially_equal(deserialize(raw_i)))
                asserts.equal(i.calcsize(), deserialize(raw_i).calcsize())
                i = deserialize(raw_i)

    @fixture_test
    def serially_equal(self):
        i0, *instances = self.serializable_instances
        mismatches = [
                i 
                for i in instances 
                if issubclass(type(i), type(i0)) and not i.serially_equal(i0)]
        for i in mismatches:
            serialize = type(i).serialize
            deserialize = type(i).deserialize
            asserts.false(deserialize(serialize(i)).serially_equal(i0))
            asserts.false(deserialize(serialize(i0)).serially_equal(i))
        
