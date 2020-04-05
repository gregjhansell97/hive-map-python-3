#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

from hmap.interface import SerializationInterface


class Topic(SerializationInterface):
    @abstractmethod
    def __hash__(self):
        raise NotImplementedError
    @abstractmethod
    def __eq__(self):
        raise NotImplementedError
    def __neq(self, other):
        return not(self == other)

    @abstractmethod
    def expose(self):

