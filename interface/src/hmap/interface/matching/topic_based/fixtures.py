#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import random 

from hmap.interface import asserts
from hmap.interface.matching.fixtures import FMatching
from hmap.interface.fixtures import fixture_test

class FTopicBasedMatching(FMatching):
    @property
    def instances(self):
        super().instances + topics(5) + messages(5)
    def get_callback(self):
        def cb(tcontent, mcontent):
            cb.log.append((tcontent, mcontent))
        cb.log = []
        return cb

    def interests(self, n):
        """List of n orthogonal Interest instances"""
        topics = self.topics(n)
        return [self.Interest([t]) for t in topics]
    def subscriptions(self, n):
        """List of n Subscription instances with callbacks from get_callback"""
        topics = self.topics(n)
        return [
                self.Subscription(t.content, self.get_callback())
                for t in topics]
    def relevant_events(self, n, i):
        events = []
        for m in self.msgs(n):
            t = random.choice(i.topics)
            events.append(self.Event(t.content, m.content))
        return events
    def irrelevant_events(self, n, i):
        events = []
        topics = self.topics(n + len(i.topics))
        for t in i.topics:
            topics.remove(t)
        topics = topics[:n]
        for t, m in zip(topics, self.msgs(n)):
            events.append(self.Event(t.content, m.content))
    @abstractmethod
    def topics(self, n):
        """List of n unique topics"""
        raise NotImplementedError
    @abstractmethod
    def msgs(self, n):
        """List of n unique messages"""
        raise NotImplementedError

    @fixture_test
    def notify_behavior(self):
        s =  self.subscriptions(1)[0]
        events = self.events(30)
        for e in events:
            s.notify(e)
            assert s.callback.log[-1] == (e.topic.content, e.msg.content)
        asserts.equal(len(s.callback.log), len(events))
    @fixture_test
    def topic_preservation(self):
        S = self.Subscription
        topics = self.topics(10)
        subs = [S(t.content, self.get_callback()) for t in topics]
        # topics can be accessed
        for s, t in zip(subs, topics):
            asserts.equal(s.topic, t.content)

