#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import weakref

from hmap.interfaces import SerializationInterface


class Event(SerializationInterface):
    """Base class for Event creation in the pub-sub system"""

    pass


class Subscription(SerializationInterface):
    """Base class for Subscription in the pub-sub system. The data that a
    subscription holds is considered to be immutable: breaking this assumption
    can cause issues with the get_matches of the Subscriptions class
    """

    def __init__(self):
        self.__owners = [] # owners of subscription class

    @property
    def owners(self):
        """List of weak references of Subscriptions the own the Subscription"""
        # weak references are used to avoid circular references
        return self.__owners

    def cancel(self):
        """Invalidates subscription so that it no longer can be delivered"""
        # remove from owners list
        for r in self.__owners:
            o = r()  # dereference weakref
            if o is None:
                continue
            o.remove(self)  # remove oneself as a subscription

    @abstractmethod
    def notify(self, event):
        """Notifies a subscription about an event it would be interested in
        
        Args:
            event(Event): event subscription would be interested in
        """
        raise NotImplementedError


class Subscriptions(SerializationInterface):
    """Base class for managing multiple subscriptions"""

    def add(self, subscription):
        """Adds subscription to the group of subscriptions

        Args:
            subscription(Subscription): subscription being added to group of 
                subscriptions
        """
        subscription.owners.append(weakref.ref(self))
        self.on_add(subscription)

    def remove(self, subscription):
        """Removes subscription from the group of subscriptions if it exists
        
        Args:
            subscription(Subscription): subscription being removed
        """
        self.on_remove(subscription)

    @abstractmethod
    def matches(self, event):
        """Gets a iteralable object of subscriptions that match an event

        Args:
            event(Event): matching event

        Returns:
            (object): iterable object of subscriptions event matches
        """
        raise NotImplementedError

    @abstractmethod
    def on_add(self, subscription):
        """Invoked after add method is; same argument and return type as add"""
        raise NotImplementedError

    @abstractmethod
    def on_remove(self, subscription):
        """Invoked after remove is, same argument and return type as remove"""
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
    def Subscriber(self):
        """Subscription implementation for the matching algorithm"""
        raise NotImplementedError

    @property
    @abstractmethod
    def Subscribers(self):
        """Subscribers implementation for the matching algorithm"""
        raise NotImplementedError
