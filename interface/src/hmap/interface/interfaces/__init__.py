#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from hmap.interface.interfaces.transceiver_interface import ITransceiver
from hmap.interface.interfaces.heartbeat_interface import IHeartbeat
from hmap.interface.interfaces.context_interface import IContext
from hmap.interface.interfaces.serialize_interface import ISerialize
from hmap.interface.interfaces.hash_interface import IHash
from hmap.interface.interfaces.equality_interface import IEquality

__all__ = [
        "ITransceiver", "IHeartbeat", "IContext", "ISerializer", "IHash", 
        "IEquality"]

