#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from hmap.matching.topic_based import Algorithm
# tests
from tests.matching.fixtures import FAlgorithm
from tests.matching.topic_based.fixtures.interest_fixtures import (
        FFlatIntInterest)
from tests.matching.topic_based.fixtures.sub_fixtures import (
        FFlatIntSubscription)
from tests.matching.topic_based.fixtures.event_fixtures import (
        FFlatIntPyObjEvent)

class FTopicBasedAlgorithm(FAlgorithm):
    Type = Algorithm

class FFlatIntPyObjAlgorithm(FTopicBasedAlgorithm):
    FInterest = FFlatIntInterest
    FEvent = FFlatIntPyObjEvent
    FSubscription = FFlatIntSubscription
    @classmethod
    def instances(cls, num):
        return [Algorithm("FlatInt", "PyObj") for i in range(num)]

base_fixtures = {FTopicBasedAlgorithm}
impl_fixtures = {FFlatIntPyObjAlgorithm}
