#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

from hmap.interface.matching.traits import Serializable, Hashable

class Topic(Serializable):
    def __repr__(self):
        return f"{type(self).__name__}({self.content})"

    def serially_equal(self, t):
        return self.content == t.content

    @property
    @abstractmethod
    def content(self):
        raise NotImplementedError

class HashableTopic(Topic, Hashable):
    def __hash__(self):
        return hash(self.content)
    def __eq__(self, other):
        return self.content == other.content


class Msg(Serializable):
    def __repr__(self): 
        return f"{type(self).__name__}({self.content})"
    
    def serially_equal(self, t):
        return self.content == t.content

    @property
    @abstractmethod
    def content(self):
        raise NotImplementedError
