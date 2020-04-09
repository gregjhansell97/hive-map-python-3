#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import pytest

from hmap import matching
from hmap.matching.topic_based.msg_types import PyObj
from hmap.matching.topic_based.templates.event import template as event_template
from hmap.matching.topic_based.topic_types import (
        FlatInt, FlatByte, FlatUInt, FlatUByte)

from tests.matching.fixtures import EventFixture

class TopicBasedEventFixture(EventFixture):
    Event = None
    events = None
    msgs = None
    topics = None

Event = event_template(FlatInt, PyObj)
msgs = ["m1", (1, 2, 3), {"A": 1}, (1, 2, 3), "m1"]
topics = [3, -1, 5, 2, 3]
events = [Event(t, m) for t, m in zip(topics, msgs)]
class FlatIntPyObjEventFixture(TopicBasedEventFixture):
    pass
FlatIntPyObjEventFixture.Event = Event
FlatIntPyObjEventFixture.msgs = msgs
FlatIntPyObjEventFixture.topics = topics
FlatIntPyObjEventFixture.events = events


class MsgFixture(ABC):
    Msg = None
    contents = None
    invalid_contents = None

class PyObjMsgFixture(MsgFixture):
    Msg = PyObj
    contents = ["A", (1, 2, "4"), MsgFixture]
    invalid_contents = [lambda x: 10]

class TopicFixture(ABC):
    Topic = None

class HashableTopicFixture(TopicFixture):
    contents = None
    invalid_contents = None

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

impl_fixtures = {PyObjMsgFixture, FlatIntTopicFixture, FlatUIntTopicFixture, 
        FlatByteTopicFixture, FlatUByteTopicFixture, FlatIntPyObjEventFixture}
base_fixtures = {MsgFixture, HashableTopicFixture, TopicBasedEventFixture, 
        TopicFixture}

