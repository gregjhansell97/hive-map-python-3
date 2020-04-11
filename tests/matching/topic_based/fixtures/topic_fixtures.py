#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import random

import pytest

from hmap.matching.topic_based.abc import Topic, HashableTopic
from hmap.matching.topic_based.topic_types import (
        FlatInt, FlatByte, FlatUInt, FlatUByte)

from tests.interfaces.fixtures import FIHash, FISerialize

class FTopic(FISerialize):
    InstanceType = Topic
    @classmethod
    def instances(cls, num):
        return [cls.InstanceType(c) for c in cls.tcontents(num)]
    @classmethod
    def equal(cls, t1, t2):
        return t1.content == t2.content
    @classmethod
    @abstractmethod
    def tcontents(cls, num):
        raise NotImplementedError
    @classmethod
    @abstractmethod
    def invalid_tcontents(cls):
        raise NotImplementedError

class FHashableTopic(FTopic, FIHash):
    InstanceType = HashableTopic
    @classmethod
    def mismatches(cls, num):
        return cls.instances(num)

class FFlatNumber(FHashableTopic):
    max_value = 0
    min_value = 0
    @classmethod
    def matches(cls, num):
        topic = random.randrange(cls.min_value, cls.max_value + 1)
        return [cls.InstanceType(topic) for _ in range(num)]
    @classmethod
    def invalid_tcontents(cls):
        return {"nope", cls.max_value + 1, cls.min_value - 1}

    @classmethod
    def tcontents(cls, num):
        return {
            cls.max_value - offset
            for offset in range(num)}

class FFlatInt(FFlatNumber):
    InstanceType = FlatInt
    max_value = (2**32)//2 - 1
    min_value = -(2**32)//2

class FFlatUInt(FFlatNumber):
    InstanceType = FlatUInt
    max_value = (2**32) - 1
    min_value = 0

class FFlatByte(FFlatNumber):
    InstanceType = FlatByte
    max_value = 127
    min_value = -128

class FFlatUByte(FFlatNumber):
    InstanceType = FlatUByte
    max_value = 255
    min_value = 0

impl_fixtures = {FFlatInt, FFlatUInt, FFlatByte, FFlatUByte}
base_fixtures = {FHashableTopic, FTopic, FFlatNumber}
