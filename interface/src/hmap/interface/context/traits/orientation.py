#!/usr/bin/env python
# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod

class X(ABC):
    @property
    @abstractmethod
    def x(self):
        raise NotImplementedError
    
class Y(ABC):
    @property
    @abstractmethod
    def y(self):
        raise NotImplementedError

class XVel(ABC):
    @property
    @abstractmethod
    def x_vel(self):
        raise NotImplementedError

class YVel(ABC):
    @property
    @abstractmethod
    def y_vel(self):
        raise NotImplementedError


__all__ = ["X", "Y", "XVel", "YVel"]
