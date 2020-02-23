#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module facilitates serialization and distributiont of information; it sets
the standards used by the other modules. Internal use only.
"""

import struct

PUB = 1
ACK = 2


class Message:
    @staticmethod
    def serialize(msg_type, header, body):
        header = struct.pack(Message.formats[msg_type], *header)
        msg_type = struct.pack("B", msg_type)
        return msg_type + header + body

    @staticmethod
    def deserialize(msg: bytes):
        # determine the message type
        print(msg)
        fmt = "B"
        size = struct.calcsize(fmt)
        (msg_type,) = struct.unpack(fmt, msg[:size])
        # move past the message type
        msg = msg[size:]
        # extract header
        fmt = Message.formats[msg_type]
        size = struct.calcsize(fmt)
        print(msg[:size])
        header = struct.unpack(fmt, msg[:size])
        # extract body
        body = msg[size:]
        return (msg_type, header, body)


Message.formats = {
    PUB: "I",  # "ideally" unique message id
    ACK: "I",  # "ideally" unique message id
}
