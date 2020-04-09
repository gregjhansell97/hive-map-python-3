#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import pytest

class EventFixture(ABC):
    events = None # event instances of class
    equal = None

class SubFixture(ABC):
    Sub = None
    Event = None
    events = None # list of events
    subs = None # list of subscriptions
    expected_interest = None #hashmap of event and a list of subscriptions interested

base_fixtures = {EventFixture, SubFixture}
impl_fixtures = set()

