#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from tests.matching.fixtures import ...
import tests.matching.topic_based as topic_based 

base_fixtures = []
base_fixtures += topic_based.base_fixtures 

impl_fixtures = []
impl_fixtures += topic_based.impl_fixtures

# sanity check 
fixtures = impl_fixtures + base_fixtures
assert(len(fixtures) == len(set(fixtures)))

__all__ = ["base_fixtures", "impl_fixtures"]
