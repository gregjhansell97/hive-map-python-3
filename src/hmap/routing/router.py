#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Router:
    """Base class responsible for delivering published messages to the 
    appropriate subscribers. This base class delivers published events local to 
    the router to subscriptions on the router.
    """

    def __init__(self, *, matching):
        """
        Args:
            matching: algorithm used for event and subscription creation
        """
        super().__init__()
        if not self.is_valid_matching(matching):
            raise ValueError("Invalid matching algorithm")
        self.__matching = matching
        self.__subscriptions = matching.Subscriptions()

    @property
    def subscriptions(self):
        """Subscriptions local publishers and subscribers are interested in"""
        return self.__subscriptions

    @property
    def matching(self):
        """Algorithm used for event and subscription creation"""
        return self.__matching

    def publish(self, *args, **kwargs):
        """Publishes an event. Do not override in child classes, see on_publish
        
        Args:
            *args: arguments passed to matching algorithm's Event constructor
            **kwargs: keyword arguments passed to matching algorithm's Event
                constructor
        """
        e = self.__matching.Event(*args, **kwargs)
        self.on_publish(e)

    def subscribe(self, *args, **kwargs):
        """Creates a subscription. Do not override in child classes, see
            on_subscribe 

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
        """Invoked when publish occurs local to the router

        Args:
            event: local event
        """
        for s in self.subscriptions.matches(event):
            self.notify(s)

    def on_subscribe(self, subscription):
        """Invoked when subscription is created local to the router

        Args:
            subscription: local subscription
        """
        self.__subscriptions.add(subscription)

    def is_valid_matching(self, algo):
        """Determines if matching algorithm can be used in routing protocol"""
        # TODO check to make sure it's a subclass of Matching
        return True
