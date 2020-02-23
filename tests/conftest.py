#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for hive_map.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

from tests.local_transceiver import LocalTransceiver


def pytest_generate_tests(metafunc):
    if "Transceiver" in metafunc.fixturenames:
        metafunc.parametrize("Transceiver", [LocalTransceiver])
