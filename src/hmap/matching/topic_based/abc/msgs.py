#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

from hmap.interfaces import ISerialize


class Msg(ISerialize):
    def __repr__(self): 
        return f"{type(self)}({self.expose()})"
    @property
    @abstractmethod
    def content(self):
        raise NotImplementedError
    def __eq__(self, other):
        return self.content == other.content
