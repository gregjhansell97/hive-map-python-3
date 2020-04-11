#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import random

import pytest

from hmap.matching.topic_based.abc import TopicBasedEvent
from hmap.matching.topic_based.templates.event import template as event_template
# tests
from tests.matching.fixtures import FEvent
from tests.matching.topic_based.fixtures.topic_fixtures import FFlatInt
from tests.matching.topic_based.fixtures.msg_fixtures import FPyObj

class FTopicBasedEvent(FEvent):
    InstanceType = TopicBasedEvent
    @classmethod
    def instances(cls, num_events):
        events_per_topic = 5
        num_topics = (num_events//events_per_topic) + 1
        topics = [t.content for t in cls.topics(num_topics)]
        msgs = [m.content for m in cls.msgs(num_events)]
        E = cls.InstanceType

        return [
                E(topics[i%len(topics)], random.choice(msgs)) 
                for i in range(num_events)]
    @classmethod
    def equal(cls, e1, e2):
        return (e1.msg.content == e2.msg.content and 
                e1.topic.content == e2.topic.content)
    @classmethod
    @abstractmethod
    def topics(cls, num): 
        raise NotImplementedError
    @classmethod
    @abstractmethod
    def msgs(cls, num):
        raise NotImplementedError

class FFlatIntPyObjEvent(FTopicBasedEvent):
    InstanceType = event_template(FFlatInt.InstanceType, FPyObj.InstanceType)
    @classmethod
    def topics(cls, num): 
        return FFlatInt.instances(num)
    @classmethod
    def msgs(cls, num):
        return FPyObj.instances(num)

base_fixtures = {FTopicBasedEvent}
impl_fixtures = {FFlatIntPyObjEvent}
