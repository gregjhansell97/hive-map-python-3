#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.contexts import Context


class PyContext:
    def serialize_message(msg):
        raise NotImplementedError
    def deserialize_message(raw_data):
        raise NotImplementedError
    def serialize_topic(topic):
        raise NotImplementedError
    def deserialize_topic(raw_data):
        raise NotImplementedError
    def is_subtopic(topic, subtopic):
        raise NotImplementedError
