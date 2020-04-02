#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class Event(ABC):
    @staticmethod
    @abstractmethod
    def serialize(event):
        raise NotImplementedError
    @staticmethod
    @abstractmethod
    def deserialize(raw_data):
        raise NotImplementedError

