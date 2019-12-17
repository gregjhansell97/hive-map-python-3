#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for Msg and AbstractHeader
"""

import pytest

from hmap.messages import AbstractHeader


class Header(AbstractHeader):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    @staticmethod
    def fmt():
        return "BBI"
    @property
    def data(self):
        return (self.a, self.b, self.c)

def test_header_initialization():
    """
    Basic creation of a header
    """
    h = Header(0, 255, 0xFFFFFFFF)

def test_header_serialization_and_deserialization():
    """
    Attempt to serialize a header and then deserialize it: there should be no
    difference between the serialized and deserialized header
    """
    h = Header(0, 255, 0xFFFFFFFF)
    raw_msg = Header.serialize(h, b"hello world")
    header, body = Header.deserialize(raw_msg)
    assert header.a == 0
    assert header.b == 255
    assert header.c == 0xFFFFFFFF
    assert body == b"hello world"
