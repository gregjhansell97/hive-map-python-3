#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import weakref

from hmap.interface.matching.traits import Serializable, Equality

class Interest(Serializable):
    """Base class for an interest in the pub-sub system"""
    class Map:
        """Base class for a datastructure that maps interests to values""" 
        @property
        @abstractmethod
        def interests():
            """Returns the interests of every value"""
            raise NotImplementedError
        @abstractmethod
        def add(self, interest, value):
            """Links interest to the value"""
            raise NotImplementedError
        @abstractmethod
        def remove(self, interest, value):
            """Removes connection between interest and value"""
            raise NotImplementedError
        @abstractmethod
        def match(self, event):
            """Returns all values that interests match the event specified"""
            raise NotImplementedError

class Event(Serializable):
    """Base class for Event creation in the pub-sub system"""
    pass

class Subscription:
    """Base class for Subscription in the pub-sub system"""
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
