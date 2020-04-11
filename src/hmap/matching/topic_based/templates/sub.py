#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.matching.topic_based.abc.subs import HashableTopicBasedSub
from hmap.matching.topic_based.abc.topics import HashableTopic


# T for Topic NOTE do not rename it to Topic
def template(T):
    """Many Topic combinations cannot write them all out, template function 
    creates subscription classes of a certain Topic 
    """
    if T in template.sub_templates:
        return template.sub_templates[T]

    if issubclass(T, HashableTopic):
        class S(HashableTopicBasedSub):
            """TODO DESCRIPTION"""
            Topic = T
            # inner class needs reference too
            class Collection(HashableTopicBasedSub.Collection):
                Topic = T
        S.Collection.Sub = S
    else:
        raise TypeError(f"{T}'s default impl is not supported")

    template.sub_templates[T] = S
    return S


template.sub_templates = {}
