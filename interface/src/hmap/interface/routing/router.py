#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from hmap.interface.matching import Matcher

class Router(ABC):
    """The router is responsible for delivering events published locally to 
    other routers and delivering externally received events to local 
    subscriptions. Refer to <link> for more information.
    """

    def __init__(self, *, matcher):
        """
        Args:
            matching: algorithm used for event and subscription creation
        """
        super().__init__()
        if not self.is_valid_matcher(matcher):
            raise ValueError("Invalid matching algorithm")
        # private classes
        self.__Interest = matcher.Interest
        self.__Event = matcher.Event
        self.__Sub = matcher.Subscription
        self.__matcher = matcher
        # private helpers 
        self.__matcher = matcher
        self.__local_subs = self.__Interest.Map()
        # TODO add to a list of weak-references of routers that
        # get stopped at the end if not already garbage collected!
    @property
    def local_interests(self):
        """List of interests of local subscriptions"""
        return self.__local_subs.interests
    @property
    def matcher(self):
        """Algorithm used for event, subscription and interest creation"""
        return self.__matcher
    def publish(self, *args, **kwargs):
        """Creates an event from the arguments specified, notifies all local
        subscriptions and the routing algorithm
        """
        e = self.__Event(*args, **kwargs)
        # notify subscriptions
        self.notify_subscriptions(e)
        # notify router
        self.notify_router(e)
    def subscribe(self, *args, **kwargs):
        """Creates a new subscription from arguments specified: the subscription
        created is notified when an event matches their criteria.

        Returns:
            A token used to unsubscribe

        Raises:
            (TypeError): invocation when inactive
        """
        s = self.__Sub(*args, **kwargs)
        self.__local_subs.add(s.interest, s)
    def unsubscribe(self, token):
        """Removes the subscription corresponding to the token from the list of
        local subscriptions

        Args:
            token: token returned by self.subscribe

        Raises:
            (KeyError): subscription was not removed successfully
        """
        # token is a subscription instance
        self.__local_subs.remove(token.interest, token)
    def notify_subscriptions(self, event):
        """Notifies all local subscriptions of an event"""
        # TODO executor
        for s in self.__local_subs.match(event):
            s.notify(event)
    @abstractmethod
    def notify_router(self, event):
        """Notifies implementation of router of a locally published event. Must
        be overriden for specific behavior
        """
        raise NotImplementedError
    def close(self):
        """Idempotent method that stops the router, all behavior after, except for
        invoking stop again, is undefined"""
        pass
    def is_valid_matcher(self, matcher):
        """Determines if matching algorithm can be used in routing protocol"""
        return issubclass(matcher.__class__, Matcher)
