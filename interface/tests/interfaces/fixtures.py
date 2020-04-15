#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.interfaces import IEquality, IHash, ISerialize

from tests.fixtures import FABC, abstractmethod

class FInterface(FABC):
    pass

class FIEquality(FInterface):
    Type = IEquality
    @classmethod
    @abstractmethod
    def matches(cls, num):
        """list of instances that are all equal"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def mismatches(cls, num):
        """list of instances that are not equal"""
        raise NotImplementedError

class FIHash(FIEquality):
    Type = IHash

class FISerialize(FInterface):
    Type = ISerialize
    @classmethod
    @abstractmethod
    def equal(cls, i1, i2):
        """compare to instances for serialization equality"""
        raise NotImplementedError

base_fixtures = {FInterface, FIEquality, FIHash, FISerialize}
impl_fixtures = set()
