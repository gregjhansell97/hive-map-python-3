#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from abc import ABC, abstractmethod

from hmap.interface.matching.traits.equality import Equality

class Hashable(Equality):
    @abstractmethod
    def __hash__(self):
        raise NotImplementedError
