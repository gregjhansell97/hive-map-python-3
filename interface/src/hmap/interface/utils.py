#!/usr/bin/env python
# -*- coding: utf-8 -*-



def has_traits(obj, traits):
    for t in traits:
        if not issubclass(type(obj), t):
            return False
    return True

