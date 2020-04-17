#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

_logger = logging.getLogger("hmap-interface")

def equal(v1, v2):
    if v1 == v2:
        return
    else:
        _logger.error(f"assert {v1} == {v2} failed!")
        raise AssertionError

def not_equal(v1, v2):
    if v1 != v2:
        return
    else:
        _logger.error(f"assert {v1} == {v2} failed!")
        raise AssertionError
