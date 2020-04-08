#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from hmap import matching


@pytest.fixture
def MatchingAlgorithm():
    A = matching.TopicBased("FlatInt", "PyObj")
    return A.Sub, A.Event, A.SubCollection
