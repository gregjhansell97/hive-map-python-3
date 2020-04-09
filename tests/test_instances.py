#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

def test_types(FABC):
    instances = FABC.instances()
    types = set()
    for F in FABC.mro():
        try:
            if F.types is not None:
                types.update(set(F.types))
        except AttributeError:
            pass
    print("#"*50)
    print(types)
    print("#"*50)
    for i in instances:
        for T in types:
            assert issubclass(type(i), T)

