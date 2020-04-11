#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import random

import pytest

from hmap.matching.topic_based import template
# tests
from tests.matching.fixtures import FAlgorithm
from tests.matching.topic_based.fixtures.sub_fixtures import FFlatIntSub
from tests.matching.topic_based.fixtures.event_fixtures import FFlatIntPyObjEvent

class FTopicBasedAlgorithm(FAlgorithm):
    pass

class FHashableTopicBasedAlgorithm(FTopicBasedAlgorithm):
    pass

class FFlatIntPyObjAlgorithm(FHashableTopicBasedAlgorithm):
    @classmethod
    def instances(cls, num):
        return [template("FlatInt", "PyObj") for i in range(num)]
    @classmethod
    def subs(cls, num): 
        return FFlatIntSub.instances(num)
    @classmethod
    def events(cls, num):
        return FFlatIntPyObjEvent.instances(num)

base_fixtures = {FTopicBasedAlgorithm, FHashableTopicBasedAlgorithm}
impl_fixtures = {FFlatIntPyObjAlgorithm}
