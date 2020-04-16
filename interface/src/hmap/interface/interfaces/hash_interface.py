#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from abc import ABC, abstractmethod

from hmap.interface.interfaces.equality_interface import IEquality

class IHash(IEquality):
    @abstractmethod
    def __hash__(self):
        raise NotImplementedError
