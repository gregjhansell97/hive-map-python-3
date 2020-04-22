#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import random 

from hmap.testing import asserts
from hmap.testing.matching.fixtures import FMatching
from hmap.testing.fixtures import fixture_test

class FTopicBasedMatching(FMatching):
    @property
    def instances(self):
        super().instances + topics(5) + messages(5)
    @property
    def Topic(self):
        return self.Event.Topic
    @property
    def Msg(self):
        return self.Event.Msg
    def get_callback(self):
        def cb(tcontent, mcontent):
            cb.log.append((tcontent, mcontent))
        cb.log = []
        return cb

    def interest_args_kwargs(self, n):
        # args = [t]
        # kargs = {}
        return [(([t],), {}) for t in self.topics(n)]

    def subscription_args_kwargs(self, n):
        return [
                (args + (self.get_callback(),), {})
                for args in self.topic_args(n)]

    def relevant_event_args_kwargs(self, n, i):
        event_args_kwargs = []
        for margs in self.msg_args(n):
            t = random.choice(i.topics)
            event_args_kwargs.append(((t.content, margs), {}))
        return event_args_kwargs

    def irrelevant_event_args_kwargs(self, n, i):
        event_args_kwargs = []
        topics = self.topics(n + len(i.topics))
        for t in i.topics:
            topics.remove(t)
            topics = topics[:n]
        for t, m in zip(topics, self.msgs(n)):
            event_args_kwargs.append(((t.content, m.content), {}))

    def topics(self, n):
        """List of n unique topics"""
        return [
                self.Topic(*args) 
                for args in self.topic_args(n)]

    def msgs(self, n):
        """List of n unique messages"""
        return [
                self.Msg(*args)
                for args in self.msg_args(n)]

    @abstractmethod
    def topic_args(self, n):
        """List of tuples of constructor arguments for n unique topics"""
        raise NotImplementedError

    @abstractmethod
    def msg_args(self, n):
        """List of tuples of constructor arguments for n unique messages"""
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

