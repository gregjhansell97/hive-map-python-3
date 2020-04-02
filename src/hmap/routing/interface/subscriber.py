#!/usr/bin/env python
# -*- coding: utf-8 -*-

# may need to handle subscriptions
# callbacks: list of callback and their subscriptions

class Subscriber(Component):
    """Responsible for subscribing a callback to a topic"""
    def on_recv(self, raw_data, event=None):
        if event is None:
            event = self.context.Event.deserialize(raw_data)
        self.subscription.pursue(event)

    def subscribe(self, *args, **kwargs):
        # topic algorithm needs to be subscriber specific
        Subscription = self.context.matching_algorithm.Subscription
        s = Subscription(*args, **kwargs)
        self.subscription.merge(s)
        return s








