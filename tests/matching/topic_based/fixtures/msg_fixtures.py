#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import pytest

from hmap.matching.topic_based.abc import Msg
from hmap.matching.topic_based.msg_types import PyObj

from tests.interfaces.fixtures import FISerialize

class FMsg(FISerialize):
    InstanceType = Msg
    @classmethod
    def equal(cls, m1, m2):
        return m1.content == m2.content

class FPyObj(FMsg):
    InstanceType = PyObj
    @classmethod
    def instances(cls):
        return [PyObj("A"), PyObj((1, 2, 3)), PyObj(FMsg)]

base_fixtures = {FMsg}
impl_fixtures = {FPyObj}
