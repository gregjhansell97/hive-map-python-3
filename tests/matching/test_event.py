#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from collections import defaultdict
import math

import pytest

from hmap.interfaces import serialize_interface


def test_event_interfaces(EventFixture):
    """verifies all methods function as expected"""
    matches = []
    events = list(EventFixture.events)
    # creates matches
    while events:
        event = events.pop()
        # doesn't match any before (otherwise wouldn't be here)
        matches.append((event,))
        # go through remaining
        i = 0
        while i in range(len(events)):
            if event == events[i]: # found a match
                matches[-1] += (events.pop(i),)
                continue
            i += 1

    # verify interfaces are happy with event
    serialize_interface.assert_consistency(matches) # ISerialize


