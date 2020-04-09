#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import pytest

#from hmap import matching
from hmap.matching.topic_based.abc import Msg
from hmap.matching.topic_based.msg_types import PyObj
#from hmap.matching.topic_based.templates.event import template as event_template
#from hmap.matching.topic_based.templates.sub import template as sub_template
#from hmap.matching.topic_based.topic_types import (
#        FlatInt, FlatByte, FlatUInt, FlatUByte)

#from tests.matching.fixtures import EventFixture, SubFixture
from tests.interfaces.fixtures import FIHash, FISerialize

'''
class TopicBasedSubFixture(SubFixture):
    Sub = None
    Event = None
    events = None
    subs = None
    expected_interest = None

Sub = sub_template(FlatInt)
Event = event_template(FlatInt, PyObj)
topics = [i for i in range(10)] + [i for i in range(20)]
messages = [f"msg{i}" for i in range(30)]
events = [Event(t, m) for t, m in zip(topics, messages)]
subs = [Sub(t) for t in zip(topics)]
expected_interest = {}
for e in events:
    expected_interest[e] = [s for s in subs if s.topic == e.topic]
class FlatIntPyObjSubFixture(TopicBasedSubFixture):
    Sub = Sub
    Event = events
    topics = topics
    messages = messages
    events = events
    subs = subs
    expected_interest = expected_interest

class TopicBasedEventFixture(EventFixture):
    Event = None
    equal = None
    equal = lambda e1, e2: e1.msg == e2.msg and e1.topic == e2.topic
    events = None
    msgs = None
    topics = None

Event = event_template(FlatInt, PyObj)
msgs = ["m1", (1, 2, 3), {"A": 1}, (1, 2, 3), "m1"]
topics = [3, -1, 5, 2, 3]
events = [Event(t, m) for t, m in zip(topics, msgs)]
class FlatIntPyObjEventFixture(TopicBasedEventFixture):
    Event = Event
    msgs = msgs
    topics = topics
    events = events

'''

class FMsg(FISerialize):
    types = [Msg]
    @classmethod
    def equal(cls, m1, m2):
        m1.content == m2.content
    #Msg = None
    #equal = lambda m1, m2: m1 == m2
    #contents = None
    #invalid_contents = None

class FPyObj(FMsg):
    types = [PyObj]
    @classmethod
    def instances(cls):
        return [PyObj("A"), PyObj((1, 2, 3)), PyObj(FMsg)]
    #Msg = PyObj
    #contents = ["A", (1, 2, "4"), MsgFixture]
    #invalid_contents = [lambda x: 10]

'''

class TopicFixture(ABC):
    Topic = None
    contents = None
    invalide_contents = None

class HashableTopicFixture(TopicFixture):
    equal = lambda t1, t2: t1 == t2
    contents = None

class FlatIntTopicFixture(HashableTopicFixture):
    Topic = FlatInt
    contents = [-(2**32)//2, -42, 0, 32, (2**32)//2 - 1]
    invalid_contents = [-(2**32)//2 - 1, (2**32)//2]

class FlatUIntTopicFixture(HashableTopicFixture):
    Topic = FlatUInt
    contents = [0, 32, (2**32) - 1]
    invalid_contents = [-1, 2**32]

class FlatByteTopicFixture(HashableTopicFixture):
    Topic = FlatByte
    contents = [-128, -42, 0, 32, 127]
    invalid_contents = [-129, 128]

class FlatUByteTopicFixture(HashableTopicFixture):
    Topic = FlatUByte
    contents = [0, 32, 255]
    invalid_contents = [-1, 256]

impl_fixtures = [PyObjMsgFixture, FlatIntTopicFixture, FlatUIntTopicFixture, 
        FlatByteTopicFixture, FlatUByteTopicFixture, FlatIntPyObjEventFixture]
base_fixtures = [MsgFixture, HashableTopicFixture, TopicBasedEventFixture, 
        TopicFixture]
'''
