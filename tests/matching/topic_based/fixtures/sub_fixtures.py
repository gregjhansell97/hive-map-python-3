#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import random

import pytest

from hmap.matching.topic_based.abc import TopicBasedSub
from hmap.matching.topic_based.templates.sub import template as sub_template
# tests
from tests.matching.fixtures import FSub, FSubCollection
from tests.matching.topic_based.fixtures.topic_fixtures import FFlatInt

class FTopicBasedSubCollection(FSubCollection):
    InstanceType = TopicBasedSub.Collection
    @classmethod
    def equal(cls, sub1, sub2):
        contents1 = [s.topic.content for s in sub1]
        contents2 = [s.topic.content for s in sub2]
        if len(contents1) != len(contents2):
            return False
        for c in contents1:
            try:
                contents2.remove(c)
            except ValueError:
                return False
        return len(contents2) == 0

class FTopicBasedSub(FSub):
    InstanceType = TopicBasedSub
    @classmethod
    def get_callback(cls):
        def cb(topic, msg):
            cb.log.append((topic, msg))
        cb.log = []
        return cb
    @classmethod
    def instances(cls, num_subs):
        subs_per_topic = 5
        num_topics = num_subs // subs_per_topic + 1
        topics = cls.topics(num_topics)
        S = cls.InstanceType
        return [
                S(topics[i%len(topics)].content, cls.get_callback()) 
                for i in range(num_subs)]
    @classmethod
    def equal(cls, s1, s2):
        return (s1.topic.content == s2.topic.content)
    @classmethod
    @abstractmethod
    def topics(cls, num): 
        raise NotImplementedError

class FFlatIntSub(FTopicBasedSub):
    InstanceType = sub_template(FFlatInt.InstanceType)
    @classmethod
    def topics(cls, num): 
        return FFlatInt.instances(num)

class FFlatIntSubCollection(FTopicBasedSubCollection):
    InstanceType = sub_template(FFlatInt.InstanceType).Collection
    @classmethod
    def subs(cls, num):
        return FFlatIntSub.instances(num)

base_fixtures = {FTopicBasedSub}
impl_fixtures = {FFlatIntSub, FFlatIntSubCollection}
