#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.matching.topic_based.fixtures import FMsg, FPyObj 
#from tests.matching.fixtures import ...

base_fixtures = [FMsg]

impl_fixtures = [FPyObj]

# sanity check 
fixtures = impl_fixtures + base_fixtures
assert(len(fixtures) == len(set(fixtures)))

__all__ = ["base_fixtures", "impl_fixtures"]
