#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.interfaces import IEquality, IHash, ISerialize

from tests.fixtures import FABC, abstractmethod

class FInterface(FABC):
    pass

class FIEquality(FInterface):
    types = [IEquality]
    @classmethod
    @abstractmethod
    def matches(cls):
        """list of instances that are all equal"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def mismatches(cls):
        """list of instances that are not equal"""
        raise NotImplementedError

class FIHash(FIEquality):
    types = [IHash]

class FISerialize(FInterface):
    types = [ISerialize]
    @classmethod
    @abstractmethod
    def equal(cls, i1, i2):
        """compare to instances for serialization equality"""
        raise NotImplementedError

