#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Facilitates serialization and deserialization of header-body based messages.
"""

import struct

# header types
PUB = 1
ACK = 2


class Message:
    """
    Static class that serializes and deserializes messages based on header types

    Attributes:
        formats(dict): key of header type and value of how to deserialize a
            certain type of header
    """

    @staticmethod
    def serialize(msg_type, header, body):
        """
        Serializes a message into a stream of bytes

        Args:
            msg_type(int): type of message, must be a key of Message
            header(tuple): header data must match up with msg type format
            body(bytes): raw bytes to tack on at end of header data
        """
        # serialize header
        header = struct.pack(Message.formats[msg_type], *header)
        # serialize msg_type
        msg_type = struct.pack("B", msg_type)
        # tack it all together
        return msg_type + header + body

    @staticmethod
    def deserialize(msg: bytes):
        """
        Deserialize message back into arguments passed in from Message.serialize 

        Args:
            msg(bytes): raw bytes of serialized message

        Returns:
            (msg_type, header, body): parameters specified by Message.serialize
        """
        # determine the message type
        fmt = "B"
        size = struct.calcsize(fmt)
        (msg_type,) = struct.unpack(fmt, msg[:size])
        # move past the message type
        msg = msg[size:]
        # extract header
        fmt = Message.formats[msg_type]
        size = struct.calcsize(fmt)
        header = struct.unpack(fmt, msg[:size])
        # extract body
        body = msg[size:]
        return (msg_type, header, body)


Message.formats = {
    PUB: "II",  # "ideally" unique message id and topic
    ACK: "I",  # "ideally" unique message id
}
