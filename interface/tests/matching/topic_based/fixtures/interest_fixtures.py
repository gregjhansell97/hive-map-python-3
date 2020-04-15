#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import random

import pytest

from hmap.matching.topic_based.templates import Interest
# tests
from tests.interfaces.fixtures import FIHash
from tests.matching.fixtures import FInterest
from tests.matching.topic_based.fixtures.topic_fixtures import FFlatInt

class FTopicBasedInterest(FInterest):
    Type = Interest
    FTopic = None
    @classmethod
    def instances(cls, num):
        # a topic for each interest
        I = cls.Type
        return [I([t]) for t in cls.topics(num)]
    @classmethod
    def equal(cls, i1, i2):
        topics1 = set([t.content for t in i1.topics])
        topics2 = set([t.content for t in i2.topics])
        #TODO more elaborate means of equivalency
        return topics1 == topics2
    @classmethod
    def topics(cls, num): 
        return cls.FTopic.instances(num)

class FFlatIntInterest(FTopicBasedInterest):
    Type = Interest.template_class(FFlatInt.Type)
    FTopic = FFlatInt

base_fixtures = {FTopicBasedInterest}
impl_fixtures = {FFlatIntInterest}
