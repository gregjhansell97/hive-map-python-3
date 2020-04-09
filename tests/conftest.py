#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for hive_map.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

from tests.fixtures import base_fixtures, impl_fixtures, FABC
import tests.matching as matching
import tests.interfaces as interfaces

base_fixtures |= matching.base_fixtures
base_fixtures |= interfaces.base_fixtures

impl_fixtures |= matching.impl_fixtures 
impl_fixtures |= interfaces.impl_fixtures

def pytest_generate_tests(metafunc):
    """
    Customize test functions however needed
    """
    for ImplF in impl_fixtures:
        if ImplF.__name__ in metafunc.fixturenames:
            metafunc.parametrize(ImplF.__name__, [ImplF])
    for BaseF in base_fixtures:
        if BaseF.__name__ in metafunc.fixturenames:
            # extract fixtures that are subclasses of BaseF (abstract fixture)
            fixtures = [
                    F
                    for F in impl_fixtures
                    if F not in base_fixtures and issubclass(F, BaseF)]
            metafunc.parametrize(BaseF.__name__, fixtures)
