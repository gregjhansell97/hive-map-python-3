#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from hmap.matching.topic_based import Matcher
# tests
from tests.matching.fixtures import FMatcher
from tests.matching.topic_based.fixtures.interest_fixtures import (
        FFlatIntInterest)
from tests.matching.topic_based.fixtures.sub_fixtures import (
        FFlatIntSubscription)
from tests.matching.topic_based.fixtures.event_fixtures import (
        FFlatIntPyObjEvent)

class FTopicBasedMatcher(FMatcher):
    Type = Matcher

class FFlatIntPyObjMatcher(FTopicBasedMatcher):
    FInterest = FFlatIntInterest
    FEvent = FFlatIntPyObjEvent
    FSubscription = FFlatIntSubscription
    @classmethod
    def instances(cls, num):
        return [Matcher("FlatInt", "PyObj") for i in range(num)]

base_fixtures = {FTopicBasedMatcher}
impl_fixtures = {FFlatIntPyObjMatcher}
