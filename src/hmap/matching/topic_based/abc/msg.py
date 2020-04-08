#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

from hmap.interfaces import SerializationInterface


class Msg(SerializationInterface):
    @abstractmethod
    def expose(self):
        raise NotImplementedError
