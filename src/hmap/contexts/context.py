#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

"""Facilitates comprehension of messages and topics

Idea:
    * once context is more flushe dout, I could see the idea of intersecting
        topic area and that jazz
"""


class Context:
    """Responsible for serializing topics and messages as well as determining
        message taxonomy
    """
    @abstractmethod
    def serialize_message(msg):
        """
        Args:
            msg: message being serialized
        Returns:
            (bytes): Serialized version of message
        """
        raise NotImplementedError
    @abstractmethod
    def deserialize_message(raw_data):
        """
        Args:
            raw_data(bytes): message being deserialized
        Return:
            Deserialized message
        """
        raise NotImplementedError
    @abstractmethod
    def serialize_topic(topic):
        """
        Args:
            topic: topic being serialized
        Returns:
            (bytes): Serialized version of topic
        """
        raise NotImplementedError
    @abstractmethod
    def deserialize_topic(raw_data):
        """
        Args:
            raw_data(bytes): topic being deserialized
        Returns:
            Deserialized topic
        """
        raise NotImplementedError
    @abstractmethod
    def is_subtopic(topic, subtopic):
        """Determines hierarchy of two topics

        Args:
            topic: topic in comparason
            subtopic: subtopic in comparason
        Returns:
            (bool): True if subtopic is subtopic of topic
        """
        raise NotImplementedError
