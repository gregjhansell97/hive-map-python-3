#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Router:
    def __init__(self, *, matching_algorithm):
        """
        Args:
            matching_algorithm: algorithm used for event and subscription 
                creation
        """
        super().__init__()
        if not self.is_valid_matching_algorithm(matching_algorithm):
            raise ValueError("Invalid matching algorithm")
        self.__matching = matching_algorithm
        self.__subscriptions = matching_algorithm.Subscription()
    @property
    def subscriptions(self):
        """Subscriptions local publishers and subscribers are interested in"""
        return self.__subscriptions
    @property
    def matching_algorithm(self):
        """Algorithm used for event and subscription creation"""
        return self.__matching
    def publish(self, *args, **kwargs):
        """Publishes an event
        
        Args:
            *args: arguments passed to matching algorithm's Event constructor
            **kwargs: keyword arguments passed to matching algorithm's Event
                constructor
        """
        e = self.__matching.Event(*args, **kwargs)
        self.on_publish(e)

    def subscribe(self, *args, **kwargs):
        """Creates a subscription

        Args:
            *args: arguments passed to matching algorithm's Subscription 
                constructor
            **kwargs: keyword arguments passed to matching algorithm's 
                Subscription constructor
        """
        s = self.__matching.Subscription(*args, **kwargs)
        self.on_subscription(s)
        return s
    def on_publish(self, event):
        """Invoked when publish occurs locally

        Args:
            event: local event
        """
        self.__subscriptions.pursue(event)
    def on_subscription(self, subscription):
        """Invoked when subscription is created locally

        Args:
            subscription: local subscription
        """
        self.__subscriptions.add(subscription)

    def is_valid_matching_algorithm(self, algo):
        """Determines if matching algorithm can be used in routing protocol"""
        return True

