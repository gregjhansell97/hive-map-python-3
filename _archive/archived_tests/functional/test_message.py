#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for message module
"""

from hmap.message import Message, PUB, ACK


def test_serialize():
    """
    Verify serialize message doesn't crash
    """
    Message.serialize(ACK, (127,), b"hello world")


def test_serialize_deserialize_PUB():
    """
    Verify PUB message can be serialized and deserialized
    """
    raw_data = Message.serialize(PUB, (9694, 8), b"goodbye stranger")
    msg_type, header, body = Message.deserialize(raw_data)
    assert msg_type == PUB
    assert header == (9694, 8)
    assert body == b"goodbye stranger"


def test_serialize_deserialize_ACK():
    """
    Verify SUB message can be serialized and deserialized
    """
    raw_data = Message.serialize(ACK, (9694,), b"good morning vietnam!")
    msg_type, header, body = Message.deserialize(raw_data)
    assert msg_type == ACK
    assert header == (9694,)
    assert body == b"good morning vietnam!"
