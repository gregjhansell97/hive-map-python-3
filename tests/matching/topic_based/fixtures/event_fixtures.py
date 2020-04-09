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
    def instances(cls):
        topics = cls.topics()
        msgs = cls.msgs()
        E = cls.InstanceType
        events_per_topic = 10
        num_events = events_per_topic*len(topics)
        return [
                E(topics[i%len(topics)].content, random.choice(msgs).content) 
                for i in range(num_events)]
    @classmethod
    def equal(cls, e1, e2):
        return (e1.msg.content == e2.msg.content and 
                e1.topic.content == e2.topic.content)
    @classmethod
    @abstractmethod
    def topics(cls): 
        raise NotImplementedError
    @classmethod
    @abstractmethod
    def msgs(cls):
        raise NotImplementedError

class FFlatIntPyObjEvent(FTopicBasedEvent):
    InstanceType = event_template(FFlatInt.InstanceType, FPyObj.InstanceType)
    @classmethod
    def topics(cls): 
        return FFlatInt.instances()
    @classmethod
    def msgs(cls):
        return FPyObj.instances()

base_fixtures = {FTopicBasedEvent}
impl_fixtures = {FFlatIntPyObjEvent}
