#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import weakref

from hmap.interfaces import ISerialize

class Interest(ISerialize):
    class Map:
        @property
        @abstractmethod
        def interests():
            raise NotImplementedError
        @abstractmethod
        def add(self, interest, val):
            """
            """
            raise NotImplementedError
        @abstractmethod
        def remove(self, interest, val):
            """
            """
            raise NotImplementedError
        @abstractmethod
        def match(self, event):
            """
            """
            raise NotImplementedError

class Event(ISerialize):
    """Base class for Event creation in the pub-sub system"""
    pass

class Subscription:
    """Base class for Subscription in the pub-sub system. The data that a
    subscription holds is considered to be immutable: breaking this assumption
    can cause issues with the get_matches of the Subscriptions class

    ALSO it seems impractical to have subs themselves be serializable, like
    when exactly are you transmitting subscritions... never! because you would
    lose the callback in the process which is the important part of a
    subscription.
    """
    def __init__(self, interest):
        self.__interest = interest
    @property
    def interest(self):
        return self.__interest
    @abstractmethod
    def notify(self, event):
        """Notifies a subscription about an event it would be interested in
        
        Args:
            event(Event): event subscription would be interested in
        """
        raise NotImplementedError

class Matcher(ABC):
    """Base class all matching algorithms follow"""
    @property
    @abstractmethod
    def Interest(self): 
        raise NotImplementedError

    @property
    @abstractmethod
    def Event(self):
        """Event implementation for the matching algorithm"""
        raise NotImplementedError

    @property
    @abstractmethod
    def Subscription(self):
        """Subscription implementation for the matching algorithm"""
        raise NotImplementedError

    def __ne__(self, other): 
        return not (self == other)
    def __eq__(self, other):
        return ( self.Interest is other.Interest and 
                self.Event is other.Event and 
                self.Subscription is other.Subscription)
