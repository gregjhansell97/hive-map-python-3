#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tests.matching.topic_based.fixtures.msg_fixtures as msg_fixtures
import tests.matching.topic_based.fixtures.topic_fixtures as topic_fixtures
import tests.matching.topic_based.fixtures.event_fixtures as event_fixtures
import tests.matching.topic_based.fixtures.sub_fixtures as sub_fixtures

base_fixtures = set()
base_fixtures |= msg_fixtures.base_fixtures
base_fixtures |= topic_fixtures.base_fixtures
base_fixtures |= event_fixtures.base_fixtures
base_fixtures |= sub_fixtures.base_fixtures

impl_fixtures = set()
impl_fixtures |= msg_fixtures.impl_fixtures
impl_fixtures |= topic_fixtures.impl_fixtures
impl_fixtures |= event_fixtures.impl_fixtures
impl_fixtures |= sub_fixtures.impl_fixtures

fixtures = base_fixtures.union(impl_fixtures)
__all__ = ["base_fixtures", "impl_fixtures"]
#TODO: __all__ += [F for F in fixtures]
