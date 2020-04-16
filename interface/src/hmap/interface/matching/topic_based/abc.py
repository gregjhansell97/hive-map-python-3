#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

from hmap.interface.interfaces import ISerialize, IHash

class Topic(ISerialize):
    def __repr__(self):
        return f"{type(self).__name__}({self.content})"

    @property
    @abstractmethod
    def content(self):
        raise NotImplementedError

class HashableTopic(Topic, IHash):
    def __hash__(self):
        return hash(self.content)
    def __eq__(self, other):
        return self.content == other.content


class Msg(ISerialize):
    def __repr__(self): 
        return f"{type(self).__name__}({self.content})"
    @property
    @abstractmethod
    def content(self):
        raise NotImplementedError
