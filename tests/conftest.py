#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for hive_map.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

from hmap.routing import Router
from hmap.matching.topic_based.topic_types import (
        FlatInt, 
        FlatByte, 
        FlatUInt, 
        FlatUByte)

def pytest_generate_tests(metafunc):
    """
    Customize test functions however needed
    """
    if "Router" in metafunc.fixturenames:
        # parameterize Router class
        routers = [Router]
        metafunc.parametrize("Router", routers)
    elif "FlatNumber" in metafunc.fixturenames:
        # parameterize FlatNumber classes
        topic_types = [FlatInt, FlatByte, FlatUInt, FlatUByte]
        metafunc.parametrize("FlatNumber", topic_types)
