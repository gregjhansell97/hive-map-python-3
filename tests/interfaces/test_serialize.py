#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

def test_serialization_equality(FISerialize):
    instances = FISerialize.instances()
    equal = FISerialize.equal
    serialize = instances[0].__class__.serialize
    deserialize = instances[0].__class__.deserialize
    calcsize = instances[0].__class__.calcsize

    layers = 5
    for i in instances:
        for _ in range(layers):
            raw_i = serialize(i)
            assert len(raw_i) == calcsize(i)
            assert equal(i, deserialize(raw_i))
            raw_i += raw_i + b"DEADBEEF"
            assert equal(i, deserialize(raw_i))
            assert calcsize(i) == calcsize(deserialize(raw_i))
            i = deserialize(raw_i)
