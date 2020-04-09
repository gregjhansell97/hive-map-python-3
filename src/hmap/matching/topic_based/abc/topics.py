#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

from hmap.interfaces import ISerialize, IHash

class Topic(ISerialize):
    def __repr__(self):
        return f"{type(self)}({self.content})"

    @property
    @abstractmethod
    def content(self):
        raise NotImplementedError

class HashableTopic(Topic, IHash):
    pass
