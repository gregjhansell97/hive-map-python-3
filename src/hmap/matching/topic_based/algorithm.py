#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching import abc
from hmap.matching.topic_based.abc import Topic as BaseTopic 
from hmap.matching.topic_based.abc import Msg as BaseMsg
# for templating
from hmap.matching.topic_based.templates import Event
from hmap.matching.topic_based.templates import Subscription
from hmap.matching.topic_based.templates import Interest
# for extracting Topic & Msg from string
import hmap.matching.topic_based.topic_types as topic_types
import hmap.matching.topic_based.msg_types as msg_types


lock = Lock() # module level lock for all algorithms
class Algorithm(abc.Algorithm):
    def __init__(self, Topic, Msg):
        # import topics if not explicitly given
        if type(Topic) is str:
            try:
                Topic = getattr(topic_types, Topic)
            except AttributeError:
                raise TypeError("invalid topic type")
        if type(Msg) is str:
            try:
                Msg = getattr(msg_types, Msg)
            except AttributeError:
                raise TypeError("invalid message type")
        # must inherit from appropriate base classes
        if not issubclass(Topic, BaseTopic):
            raise TypeError("invalid topic type")
        if not issubclass(Msg, BaseMsg):
            raise TypeError("invalid message type")
        with lock:
            self.__I = Interest.template_class(Topic)
            self.__E = Event.template_class(Topic, Msg)
            self.__S = Subscription.template_class(self.__I)
    @property
    def Interest(self):
        return self.__I
    @property
    def Event(self):
        return self.__E
    @property
    def Subscription(self):
        return self.__S
