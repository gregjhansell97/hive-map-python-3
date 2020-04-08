#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock

from hmap.matching.topic_based import abc


# T for Topic NOTE do not rename it to Topic
def template(T):
    """Many Topic combinations cannot write them all out, template function 
    creates subscription classes of a certain Topic 
    """
    with template.lock:
        if T in template.sub_templates:
            return template.sub_templates[T]

    class S(abc.TopicBasedSub):
        """TODO DESCRIPTION"""

        Topic = T

    with template.lock:
        if T not in template.sub_templates:
            template.sub_templates[T] = S
    return template.sub_templates[T]


template.sub_templates = {}
template.lock = Lock()
