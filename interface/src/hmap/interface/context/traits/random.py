#!/usr/bin/env python
# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod


class Uniform(ABC):
    @abstractmethod
    def random_uniform(self, a, b):
        raise NotImplementedError
