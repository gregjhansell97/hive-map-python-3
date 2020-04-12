#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from abc import ABC, abstractmethod

class ISerialize(ABC):
    @abstractmethod
    def calcsize(self):
        raise NotImplementedError
    @classmethod
    @abstractmethod
    def serialize(cls, instance):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def deserialize(cls, raw_data, lazy=False):
        raise NotImplementedError
