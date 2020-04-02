#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class Subscription(ABC):
    @staticmethod
    @abstractmethod
    def serialize(event):
        raise NotImplementedError
    @staticmethod
    @abstractmethod
    def deserialize(raw_data):
        raise NotImplementedError
    @abstractmethod
    def is_interested(event):
        raise NotImplementedError
    @abstractmethod
    def pursue(event):
        raise NotImplementedError
    @abstractmethod
    def add(subscription):
        raise NotImplementedError

   
