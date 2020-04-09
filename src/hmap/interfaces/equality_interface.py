#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from abc import ABC, abstractmethod

class IEquality(ABC):
    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError
    def __ne__(self, other):
        return not (self == other)
