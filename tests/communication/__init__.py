#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.communication.fixtures import base_fixtures, impl_fixtures
import tests.communication.transceivers as transceivers

base_fixtures |= transceivers.base_fixtures

impl_fixtures |= transceivers.impl_fixtures

__all__ = ["base_fixtures", "impl_fixtures"]

