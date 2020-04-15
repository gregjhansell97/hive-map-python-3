#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from tests.matching.fixtures import ...
from tests.matching.fixtures import base_fixtures, impl_fixtures
import tests.matching.topic_based as topic_based

base_fixtures |= topic_based.base_fixtures
impl_fixtures |= topic_based.impl_fixtures

__all__ = ["base_fixtures", "impl_fixtures"]
