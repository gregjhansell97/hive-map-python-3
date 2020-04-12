#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import pytest

def test_event_serialization_properties(FEvent):
    E = FEvent.Type
    events = FEvent.instances(10)
    serialize = E.serialize
    deserialize = E.deserialize
    # ensure serialization changes set reference
    for e in events:
        assert e != deserialize(serialize(e))

def test_interest_serialization_properties(FInterest):
    I = FInterest.Type
    interests = FInterest.instances(10)
    serialize = I.serialize
    deserialize = I.deserialize
    # ensure serialization changes set reference
    for i in interests:
        assert i == i
        assert i != deserialize(serialize(i))

def test_interest_map_properties(FInterest):
    def different(m1, m2):
        return (m1 is not m2) and (not m1 == m2) and (m1 != m2)
    I = FInterest.Type
    interests = FInterest.instances(10)
    # interests must be unique (quick sanity check
    assert len(set(interests)) == len(interests)
    # partition interests
    interests1 = interests[::2]
    interests2 = interests[1::2]
    map1 = I.Map()
    map2 = I.Map()
    # confirm both are empty
    assert len({i for i in map1.interests}) == 0
    assert len({i for i in map2.interests}) == 0
    # check to make sure different
    assert different(map1, map2)
    # add the same items to both maps
    items = []
    for i, v in zip(interests, range(len(interests))):
        items.append((i, v))
        map1.add(i, v)
        map2.add(i, v)
        # add duplicates, should have both
        map1.add(i, v)
        map2.add(i, v)
    # NOTE can't do a pairwise comparason may glob interests differently
    # NOTE no constraing on determinism (as long as the end goal is the same)
    # confirm both are not empty
    assert len({i for i in map1.interests}) > 0
    assert len({i for i in map2.interests}) > 0
    # check to make sure still different
    assert different(map1, map2)
    # remove all items from map1 and remove one more
    for i, v in items:
        map1.remove(i, v)
        map1.remove(i, v)
        map1.add(i, None)
        with pytest.raises(KeyError):
            map1.remove(i, v)
        map1.remove(i, None)
        with pytest.raises(KeyError):
            map1.remove(i, None)
    # gutted map1, should be empty
    assert len({i for i in map1.interests}) == 0
    # try to remove another item should cause a key error
    with pytest.raises(KeyError):
        map1.remove(*items[0])

def test_algorithm(FAlgorithm):
    algo = FAlgorithm.instances(1)[0]
    Interest = FAlgorithm.FInterest.Type
    Event = FAlgorithm.FEvent.Type
    Subscription = FAlgorithm.FSubscription.Type
    # check compatability
    issubclass(Interest, algo.Interest)
    issubclass(Interest.Map, algo.Interest.Map)
    issubclass(Event, algo.Event)
    issubclass(Subscription, algo.Subscription)
    # may not be able to assert much, but can crash test it
    # and test it for consistency
    events = FAlgorithm.events(30)
    subscriptions = FAlgorithm.subscriptions(10)
    map_ = Interest.Map()
    # EMPTYNESS
    for e in events:
        assert len(list(map_.match(e))) == 0
    # CONSISTENCY
    # add all subscriptions to map_ and the id of the subscription 
    # upon retrieving from different events, should have the subscription and 
    # subscription.notify method
    for s in subscriptions:
        map_.add(s.interest, s.notify)
        map_.add(s.interest, s)
    # iterate through events and test
    for e in events:
        values = set(map_.match(e))
        for v in values:
            try:
                assert v.notify in values
            except AttributeError:
                pass # not a subscription
    # remove all subscriptions
    for s in subscriptions:
        map_.remove(s.interest, s.notify)
        with pytest.raises(KeyError):
            map_.remove(s.interest, s.notify)
        map_.remove(s.interest, s)
    # EMPTYNESS
    for e in events:
        assert len(list(map_.match(e))) == 0











