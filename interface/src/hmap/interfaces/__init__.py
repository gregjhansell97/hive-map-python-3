#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from hmap.interfaces.transceiver_interface import ITransceiver
from hmap.interfaces.heartbeat_interface import IHeartbeat
from hmap.interfaces.context_interface import IContext
from hmap.interfaces.serialize_interface import ISerialize
from hmap.interfaces.hash_interface import IHash
from hmap.interfaces.equality_interface import IEquality

__all__ = [
        "ITransceiver", "IHeartbeat", "IContext", "ISerializer", "IHash", 
        "IEquality"]

