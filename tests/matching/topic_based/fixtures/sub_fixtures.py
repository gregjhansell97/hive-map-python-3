#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from hmap.matching.topic_based.templates import Subscription, Interest
# tests
from tests.matching.fixtures import FSubscription
from tests.matching.topic_based.fixtures.topic_fixtures import FFlatInt

class FTopicBasedSubscription(FSubscription):
    Type = Subscription
    FTopic = None
    @classmethod
    def get_callback(cls):
        def cb(topic, msg):
            cb.log.append((topic, msg))
        cb.log = []
        return cb
    @classmethod
    def instances(cls, num):
        S = cls.Type
        return [S(t.content, cls.get_callback()) for t in cls.topics(num)]
    @classmethod
    def equal(cls, s1, s2):
        return (s1.topic.content == s2.topic.content)
    @classmethod
    def topics(cls, num): 
        return cls.FTopic.instances(num)

class FFlatIntSubscription(FTopicBasedSubscription):
    Type = Subscription.template_class(Interest.template_class(FFlatInt.Type))
    FTopic = FFlatInt

base_fixtures = {FTopicBasedSubscription}
impl_fixtures = {FFlatIntSubscription}
