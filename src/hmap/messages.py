#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import struct


class AbstractHeader:
    """
    All headers must comply with AbstractHeader to be serializable with the Msg
    class. Also must register themselves as a header
    """
    def __init__(self):
        raise NotImplementedError
        
    @staticmethod
    @abstractmethod
    def fmt()->str:
        """
        Returns:
            description of format style specified by pythons page on structs
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self)->tuple:
        """
        Returns:
            data as a tuple being serialized by a certain fmt, should be able 
                to put into constructor
        """
        raise NotImplementedError


    

class Msg:
    """
    All messages have a header and a body. The header is meta information
    pertaining to the data and handling of the data. Factory class that
    serializes and deserializes the header and body of Msg instance. Did 
    not pickle because pickle includes an enum infront of raw bytes to
    indicate which class to use when deserializing

    Attributes:
        header: on of the header classes defined in headers
        body(bytes): raw bytes being stored
        allignment(bytes): verify the ordering of bytes to determine how to
            decifer the rest of the message
        type(int): header type being sent [10, 255], did this instead of leaning
            on enum class type because needs to work across languages
    """
    def __init__(self, header, body):
        self.header = header
        self.body = body

    @staticmethod
    def serialize(m):
        """
        """
        fmt = m.header.fmt
        data = m.header.data
        return struct.pack(fmt, *data) + m.body

    @staticmethod
    def deserialize(exp_cls, raw_data):
        """
        """
        H = exp_cls
        fmt = H.fmt
        size = struct.calcsize(fmt)
        # breakdown next header
        header = H(*struct.unpack(fmt, raw_data[:size]))
        body = raw_data[size:]
        return Msg(header, body)
