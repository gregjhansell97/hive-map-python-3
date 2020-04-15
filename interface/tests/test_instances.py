#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

def test_type(FABC):
    instances = FABC.instances(6)
    superclasses = set()
    for F in FABC.mro():
        try:
            superclasses.add(F.Type)
        except AttributeError:
            pass
    for i in instances:
        for T in superclasses:
            assert issubclass(type(i), T)

def test_instance_uniqueness(FABC):
    instances = FABC.instances(6)
    for i1 in instances:
        count =  0
        for i2 in instances:
            if i1 is i2:
                count += 1
        assert count == 1

def test_instances_uniqueness(FABC):
    instances1 = FABC.instances(6)
    instances2 = FABC.instances(6)
    for i in instances1:
        for j in instances2:
            assert i is not j
        

def test_num_instances(FABC):
    for i in range(6):
        assert len(FABC.instances(i)) == i
