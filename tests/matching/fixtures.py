#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import pytest

from hmap.matching.abc import Event, Sub, Algorithm
from tests.interfaces.fixtures import FISerialize
from tests.fixtures import FABC

class FMatchingComponent(FISerialize):
    InstanceType = object

class FEvent(FMatchingComponent):
    InstanceType = Event

class FSub(FMatchingComponent):
    InstanceType = Sub

class FSubCollection(FMatchingComponent):
    InstanceType = Sub.Collection
    @classmethod
    def instances(cls, num):
        Collection = cls.InstanceType
        subs_per_collection = 10
        subs = cls.subs(subs_per_collection*num)
        collections = [Collection() for _ in range(num)]
        for s, i in zip(subs, range(len(subs))):
            collections[i%len(collections)].add(s)
        return collections
    @classmethod
    @abstractmethod
    def subs(cls, num):
        raise NotImplementedError

class FAlgorithm(FABC):
    InstanceType = Algorithm
    @classmethod
    @abstractmethod
    def subs(cls, num):
        raise NotImplementedError
    @classmethod
    @abstractmethod
    def events(cls, num):
        raise NotImplementedError


base_fixtures = {FMatchingComponent, FEvent, FSub, FSubCollection, FAlgorithm}
impl_fixtures = set()

