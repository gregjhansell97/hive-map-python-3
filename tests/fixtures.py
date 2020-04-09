#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class FABC(ABC):
    types = []
    @classmethod
    @abstractmethod
    def instances(cls):
        """List of instances of a specific type"""
        raise NotImplementedError
