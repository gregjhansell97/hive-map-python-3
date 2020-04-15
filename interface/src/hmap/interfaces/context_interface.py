#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

from abc import ABC, abstractmethod

class IContext(ABC):
    def __init__(self, context=None):
        super().__init__()
        if not self.is_valid_context(context):
            raise ValueError("invalid context")
        self.__context = context

    @property
    def context(self):
        """Context read-only property"""
        return self.__context

    def is_valid_context(self, ctx):
        return True
