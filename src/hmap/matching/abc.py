#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import weakref

from hmap.interfaces import ISerialize


class Event(ISerialize):
    """Base class for Event creation in the pub-sub system"""

    pass


class Sub(ISerialize):
    """Base class for Subscription in the pub-sub system. The data that a
    subscription holds is considered to be immutable: breaking this assumption
    can cause issues with the get_matches of the Subscriptions class

    ALSO it seems impractical to have subs themselves be serializable, like
    when exactly are you transmitting subscritions... never! because you would
    lose the callback in the process which is the important part of a
    subscription.
    """

    @abstractmethod
    def notify(self, event):
        """Notifies a subscription about an event it would be interested in
        
        Args:
            event(Event): event subscription would be interested in
        """
        raise NotImplementedError

    class Collection(ISerialize):
        """Base class for managing multiple subscriptions"""
        # NOTE serialization does not necessarily mean component wise agreement
        # the serialization process could simply depict what the colleciton
        # embodies (like the currently interested topics...
        # subscribe option to it ... almost like a subscription...

        @abstractmethod
        def __iter__(self):
            # for iterating over all subs
            raise NotImplementedError

        @abstractmethod
        def extend(self, sub_collection):
            # addes the items of one sub_collection into another
            raise NotImplementedError

        @abstractmethod
        def add(self, subscription):
            """Adds subscription to the group of subscriptions

            Args:
                subscription(Sub): subscription being added to group of 
                    subscriptions
            """
            raise NotImplementedError

        @abstractmethod
        def remove(self, subscription):
            """Removes subscription from the group of subscriptions if it exists
        
            Args:
                subscription(Sub): subscription being removed
            """
            raise NotImplementedError

        @abstractmethod
        def matches(self, event):
            """Gets a iteralable object of subscriptions that match an event

            Args:
                event(Event): matching event

            Returns:
                (object): iterable object of subscriptions event matches
            """
            raise NotImplementedError


class Algorithm(ABC):
    """Base class all matching algorithms follow"""

    @property
    @abstractmethod
    def Event(self):
        """Event implementation for the matching algorithm"""
        raise NotImplementedError

    @property
    @abstractmethod
    def Sub(self):
        """Subscription implementation for the matching algorithm"""
        raise NotImplementedError
