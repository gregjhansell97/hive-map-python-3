#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def Callback():
    def cb(topic, msg):
        cb.log.add((topic, msg))

    cb.log = set()
    return cb
