#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class Protocol(ABC):
    """Base class for protocols
    """
    @staticmethod
    @abstractmethod
    def make_publisher(*args, **kwargs):
        """Returns: 
             (Publisher): protocol's instance of publisher"""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def make_subscriber(*args, **kwargs):
        """Returns: 
             (Subscriber): protocol's instance of subscriber"""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def make_router(*args, **kwargs):
        """Returns: 
             (Router): protocol's instance of router"""
        raise NotImplementedError

