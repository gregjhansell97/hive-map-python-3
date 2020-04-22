#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

from hmap.testing.fixtures import FHMap 


class raises:
    def __init__(self, *exceptions):
        self.__exceptions = exceptions
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type in self.__exceptions:
            return True
        elif exc_type is not None:
            return False
        else:
            raise AssertionError(f"expected {self.__exceptions}")
# TODO would be cool to show more than just line
def true(b):
    try:
        assert b
    except:
        raise
    else:
        statement = traceback.format_stack()[-2].strip()
        FHMap.logger.debug(f"success: {statement}")

def false(b):
    try:
        assert not b
    except:
        raise
    else:
        statement = traceback.format_stack()[-2].strip()
        FHMap.logger.debug(f"success: {statement}")

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
