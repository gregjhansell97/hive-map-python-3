#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import random

import pytest

from hmap.matching.topic_based.abc import Msg
from hmap.matching.topic_based.msg_types import PyObj

from tests.interfaces.fixtures import FISerialize

class FMsg(FISerialize):
    Type = Msg
    @classmethod
    def equal(cls, m1, m2):
        return m1.content == m2.content

class FPyObj(FMsg):
    Type = PyObj
    @classmethod
    def instances(cls, num):
        return [
                PyObj((i, str(i), hash(i), None))
                for i in range(num)]

base_fixtures = {FMsg}
impl_fixtures = {FPyObj}
