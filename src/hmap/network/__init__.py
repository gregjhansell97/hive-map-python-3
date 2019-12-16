#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classes that support communication between locations and destinations
"""

from hmap.network.abstract_socket import AbstractSocket
from hmap.network.local_socket import LocalSocket

__all__ = ["AbstractSocket", "LocalSocket"]
