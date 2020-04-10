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
    def instances(cls):
        Collection = cls.InstanceType
        subs = cls.subs()
        collections = [Collection() for _ in range(5)]
        assert len(subs) > len(collections), f"Need more subs than collections"
        for s, i in zip(subs, range(len(subs))):
            collections[i%len(collections)].add(s)
        collections.append(Collection()) #empty collection
        return collections
    @classmethod
    @abstractmethod
    def subs(cls):
        raise NotImplementedError

class FAlgorithm(FABC):
    InstanceType = Algorithm
    @classmethod
    @abstractmethod
    def subs(cls):
        raise NotImplementedError
    @classmethod
    @abstractmethod
    def events(cls):
        raise NotImplementedError


base_fixtures = {FMatchingComponent, FEvent, FSub, FSubCollection, FAlgorithm}
impl_fixtures = set()

