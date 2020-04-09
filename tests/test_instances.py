#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

def test_type(FABC):
    instances = FABC.instances()
    superclasses = set()
    for F in FABC.mro():
        try:
            superclasses.add(F.InstanceType)
        except AttributeError:
            pass
    for i in instances:
        for T in superclasses:
            assert issubclass(type(i), T)

