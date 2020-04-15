#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import random

import pytest

from hmap.matching.topic_based.templates import Event
# tests
from tests.matching.fixtures import FEvent
from tests.matching.topic_based.fixtures.topic_fixtures import FFlatInt
from tests.matching.topic_based.fixtures.msg_fixtures import FPyObj

#TODO make sure consistent topic, msg with FTopic and FMsg
class FTopicBasedEvent(FEvent):
    Type = Event
    FTopic = None
    FMsg = None
    @classmethod
    def instances(cls, num_events):
        events_per_topic = 5
        num_topics = (num_events//events_per_topic) + 1
        topics = [t.content for t in cls.topics(num_topics)]
        msgs = [m.content for m in cls.msgs(num_events)]
        E = cls.Type

        return [
                E(topics[i%len(topics)], random.choice(msgs)) 
                for i in range(num_events)]
    @classmethod
    def equal(cls, e1, e2):
        return (e1.msg.content == e2.msg.content and 
                e1.topic.content == e2.topic.content)
    @classmethod
    def topics(cls, num): 
        return cls.FTopic.instances(num)
    @classmethod
    def msgs(cls, num):
        return cls.FMsg.instances(num)

class FFlatIntPyObjEvent(FTopicBasedEvent):
    Type = Event.template_class(FFlatInt.Type, FPyObj.Type)
    FTopic = FFlatInt
    FMsg = FPyObj

base_fixtures = {FTopicBasedEvent}
impl_fixtures = {FFlatIntPyObjEvent}
