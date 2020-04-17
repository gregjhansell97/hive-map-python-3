#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.interface.fixtures import FHMap 

def equal(v1, v2):
    try:
        assert v1 == v2
    except:
        FHMap.logger.error(f"assert {v1} == {v2} failed!")
        raise

def not_equal(v1, v2):
    try:
        assert v1 != v2
    except:
        FHMap.logger.error(f"assert {v1} != {v2} failed!")
        raise
