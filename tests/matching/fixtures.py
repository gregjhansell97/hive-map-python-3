#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import pytest

from hmap.matching import Event, Subscription, Interest, Matcher
from tests.interfaces.fixtures import FISerialize
from tests.fixtures import FABC

class FEvent(FISerialize) :
    Type = Event

class FSubscription(FABC):
    Type = Subscription

class FInterest(FISerialize):
    Type = Interest

class FMatcher(FABC):
    Type = Matcher
    FInterest = None
    FEvent = None
    FSubscription = None
    @classmethod
    @abstractmethod
    def interests(cls, num):
        return cls.FInterest.instances(num)
    @classmethod
    @abstractmethod
    def subscriptions(cls, num):
        return cls.FSubscription.instances(num)
    @classmethod
    @abstractmethod
    def events(cls, num):
        return cls.FEvent.instances(num)


base_fixtures = {FEvent, FInterest, FSubscription, FMatcher}
impl_fixtures = set()

