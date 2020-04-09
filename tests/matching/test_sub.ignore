#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for FlatInt matching.TopicBased algorithm
"""

import pytest

def test_sub_collection(SubFixture):
    # locals 
    Sub = SubFixture.Sub
    Event = SubFixture.Event
    events = SubFixture.events
    subs = SubFixture.subs
    expected_interest = SubFixture.expected_interest
    # size requirements met
    assert len(subs) >= 2, "must have at least 6"
    divider = len(subs)/2
    # divide up subscription
    subs1 = subs[:divider]
    subs2 = subs[divider:]
    # create collections
    collection1 = Sub.Collection()
    collection2 = Sub.Collection()
    # add subscriptions to collections
    for s in subs1:
        collection1.add(s)
    for s in subs2:
        collection2.add(s)
    # check iterations
    assert set(subs1) == set([s for s in collections1])
    # check matches
    for e in events:
        expected_subs1 = {s for s in expected_interest[e] if s in subs1}
        assert expected_subs == {s for s in collections1.matches(e)}
    # merge together
    # check merge didn't screw anything up
    # remove some subscriptions and make sure that doesn't screw anything up

