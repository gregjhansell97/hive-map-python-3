#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class FABC(ABC):
    Type = object
    @classmethod
    @abstractmethod
    def instances(cls, num):
        """List of instances of a specific type"""
        raise NotImplementedError

base_fixtures = {FABC}
impl_fixtures = set()
