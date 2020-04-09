#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for hive_map.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

import tests.matching.fixtures as matching_fixtures
import tests.matching.topic_based.fixtures as topic_based_matching_fixtures

# collect impl_fixtures
impl_fixtures = matching_fixtures.impl_fixtures
impl_fixtures |= topic_based_matching_fixtures.impl_fixtures

# collect base_fixtures
base_fixtures = matching_fixtures.base_fixtures
base_fixtures |= topic_based_matching_fixtures.base_fixtures


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
