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

base_fixtures = {FMatchingComponent, FEvent, FSub}
impl_fixtures = set()

