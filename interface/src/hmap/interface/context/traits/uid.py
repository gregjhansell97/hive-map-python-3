#!/usr/bin/env python
# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod


class Bytes(ABC):
    @property
    @abstractmethod
    def uid(self):
        raise NotImplementedError
