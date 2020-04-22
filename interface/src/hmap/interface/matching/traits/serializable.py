#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from abc import ABC, abstractmethod

class Serializable(ABC):
    @abstractmethod
    def calcsize(self):
        raise NotImplementedError
    @abstractmethod
    def serially_equal(self, s):
        raise NotImplementedError
    @classmethod
    @abstractmethod
    def serialize(cls, instance):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def deserialize(cls, raw_data):
        raise NotImplementedError

