#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

from hmap.interfaces import ISerialize


class Msg(ISerialize):
    def __repr__(self): 
        return f"{type(self).__name__}({self.content})"
    @property
    @abstractmethod
    def content(self):
        raise NotImplementedError
