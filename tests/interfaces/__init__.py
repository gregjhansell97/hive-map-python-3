#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.interfaces.fixtures import (
        FInterface, FIEquality, FIHash, FISerialize)

base_fixtures = [FInterface, FIEquality, FIHash, FISerialize]
impl_fixtures = []

__all__ = ["base_fixtures", "impl_fixtures"]
