#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module facilitates serialization and distributiont of information; it sets
the standards used by the other modules. Internal use only.
"""

from abc import ABC, abstractmethod
import struct


class AbstractHeader:
    """
    All headers must comply with AbstractHeader to be serializable into bytes
    and deserialized into a header and body
    """

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def serialize(class_, header, body: bytes):
        """
        Serializes a header and body into bytes that can be deserialized later.
        A class method instead of an instance's method to match deserialize

        Args:
            header: same type as the class invoking serialize
            body: raw bytes of data to tack on to header

        Returns:
            (bytes): serialized data of header and body
        """
        fmt = class_.fmt()
        data = header.data
        return struct.pack(fmt, *data) + body

    @classmethod
    def deserialize(H, raw_data: bytes):
        """
        Converts raw_data into a header and body

        Args:
            raw_data: bytes containing both the header and body

        Returns:
            (tuple): first item is the header of the header class used to
                deserialize; second item is the body which are the remaining
                bytes
        """
        fmt = H.fmt()
        size = struct.calcsize(fmt)
        # breakdown next header
        header = H(*struct.unpack(fmt, raw_data[:size]))
        body = raw_data[size:]
        return (header, body)

    @staticmethod
    @abstractmethod
    def fmt():
        """
        Returns:
            (str): Description of format style specified by pythons page on 
                structs
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self):
        """
        Data as a tuple being serialized by a certain fmt, should be able to 
        put into constructor
        """
        raise NotImplementedError
