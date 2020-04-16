#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock
from hmap.interface.matching import Subscription as BaseSubscription

templates = {}
class Subscription(BaseSubscription):
    Interest = None
    def __init__(self, tcontent, callback):
        # topic arg lets me deserialize
        #TODO check to make sure callback is valid
        topic = self.Interest.Topic(tcontent)
        super().__init__(self.Interest([topic]))
        self.__callback = callback
    @property
    def callback(self):
        return self.__callback
    @property
    def topic(self):
        return self.interest.topics[0].content
    def notify(self, event):
        # subscription can't call None
        self.__callback(event.topic.content, event.msg.content)
    @staticmethod
    def template_class(I):
        """Many Topic combinations cannot write them all out, template function 
        creates subscription classes of a certain Interest
        """
        if I in templates:
            return templates[I]
        class S(Subscription):
            Interest = I
        templates[I] = S
        return S
