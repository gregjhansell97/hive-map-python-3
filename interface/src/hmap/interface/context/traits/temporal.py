#!/usr/bin/env python
# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod

class Time(ABC):
    @property
    @abstractmethod
    def time(self):
        raise NotImplementedError

class Sleep(ABC):
    @abstractmethod
    def sleep(self, duration):
        raise NotImplementedError

__all__ = ["Time", "Sleep"]
