#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from hmap.interface.matching.traits.serializable import Serializable
from hmap.interface.matching.traits.hashable import Hashable
from hmap.interface.matching.traits.equality import Equality

__all__ = ["Serializable", "Hashable", "Equality"]

