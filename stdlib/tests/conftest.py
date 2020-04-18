#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for std.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

import time

def pytest_report_collectionfinish(*args, **kwargs):
    time.sleep(1)
