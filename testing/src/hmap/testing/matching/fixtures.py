#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from hmap.testing import asserts
from hmap.testing.fixtures import FHMap, fixture_test
from hmap.testing.matching.traits.fixtures import FSerializable, FHashable

class FMatching(FSerializable):
    @property
    def instances(self):
        instances = self.matchers(3)
        instances += self.interests(5)
        instances += self.subscriptions(5)
        instances += self.event(5)
        return instances
    @property
    def serializable_instances(self):
        instances = self.interests(3) + self.interests(3)
        instances += self.events(3) + self.events(3)
        return instances
    @property
    def Event(self):
        return self.matchers(1)[0].Event
    @property
    def Interest(self):
        return self.matchers(1)[0].Interest
    @property
    def Subscription(self):
        return self.matchers(1)[0].Subscription
    def interests(self, n):
        """List of n orthogonal Interest instances"""
        return [
                self.Interest(*args, **kwargs)
                for args, kwargs in self.interest_args_kwargs(n)]
    def subscriptions(self, n):
        """List of n Subscription instances"""
        return [
                self.Subscription(*args, **kwargs)
                for args, kwargs in self.subscription_args_kwargs(n)]
    def events(self, n):
        """List of n events"""
        events = []
        for i in self.interests(n):
            events += self.relevant_events(1, i)
        return events
    def relevant_events(self, n, i):
        """List of n Event instances relevant to given interest"""
        return [
                self.Event(*args, **kwargs)
                for args, kwargs in self.relevant_event_args_kwargs(n, i)]
    def irrelevant_events(self, n, i):
        """List of n Event instances irrelevant to a given interest"""
        return [
                self.Event(*args, **kwargs)
                for args, kwargs in self.irrelevant_event_args_kwargs(n, i)]

    @abstractmethod
    def matchers(self, n):
        """List of n matchers of same matching algorithm"""
        raise NotImplementedError

    @abstractmethod
    def interest_args_kwargs(self, n):
        """List of n 2-d tuples of constructor arguments for interest"""
        raise NotImplementedError

    @abstractmethod
    def subscription_args_kwargs(self, n):
        """List of n 2-d tuples of constructor arguments for subscription"""
        raise NotImplementedError

    @abstractmethod
    def relevant_event_args_kwargs(self, n, i):
        """List of n 2-d tuples of constructor arguments for events relevant to
        a given interest
        """
        raise NotImplementedError

    @abstractmethod
    def irrelevant_event_args_kwargs(self, n, i):
        """List of n 2-d tuples of constructor arguemnts for events irrelevant to
        a given interest
        """
        raise NotImplementedError

    @fixture_test
    def event_serialization_properties(self):
        E = self.Event
        events = self.events(10)
        serialize = E.serialize
        deserialize = E.deserialize
        # ensure serialization changes set reference
        for e in events:
            # TODO serialization equivalence for a class
            asserts.not_equal(e, deserialize(serialize(e)))

    @fixture_test
    def interest_serialization_properties(self):
        interests = self.interests(10)
        serialize = self.Interest.serialize
        deserialize = self.Interest.deserialize
        # general serialization testing
        # ensure serialization changes set reference
        for i in interests:
            asserts.equal(i, i)
            asserts.not_equal(i, deserialize(serialize(i)))

    @fixture_test
    def interest_map_matching(self):
        interest, disinterest, nointerest = self.interests(3)
        event = self.relevant_events(1, interest)[0]
        nointerest_event = self.relevant_events(1, nointerest)[0]

        imap = self.Interest.Map()
        imap.add(interest, 1) # adding value
        imap.add(disinterest, 2) # adding value

        # get all interests that would match event
        asserts.equal(set([1]), set(imap.match(event)))
        # ensure that irrelevant doesn't trigger anything
        asserts.equal(set(), set(imap.match(nointerest_event)))
    
        # interest back isn't necessarily compatable but should end with 
        # same result
        imap.remove(disinterest, 2) # only interest remains now
        old_interests = imap.interests
        imap = interest.Map() # new imap
        for i in old_interests:
            imap.add(i, 1)
        imap.add(disinterest, 2)
        imap.add(interest, 3)
        # get all values that would match event
        asserts.equal(set([1, 3]), set(list(imap.match(event))))

    @fixture_test
    def interest_map_properties(self):
        def different(m1, m2):
            return (m1 is not m2) and (not m1 == m2) and (m1 != m2)
        I = self.Interest
        interests = self.interests(10)
        # interests must be unique (quick sanity check
        asserts.equal(len(set(interests)), len(interests))
        # partition interests
        interests1 = interests[::2]
        interests2 = interests[1::2]
        map1 = I.Map()
        map2 = I.Map()
        # confirm both are empty
        asserts.equal(len({i for i in map1.interests}), 0)
        asserts.equal(len({i for i in map2.interests}), 0)
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
            key_error = False
            try:
                map1.remove(i, v)
            except KeyError:
                pass
            else:
                assert False # needs to throw a key error

            map1.remove(i, None)
            try:
                map1.remove(i, None)
            except KeyError:
                pass
            else:
                assert False
        # gutted map1, should be empty
        assert len({i for i in map1.interests}) == 0
        # try to remove another item should cause a key error
        try:
            map1.remove(*items[0])
        except KeyError:
            pass
        else:
            assert False

    @fixture_test
    def matcher_properties(self):
        Interest = self.Interest
        Event = self.Event
        Subscription = self.Subscription
        matchers = self.matchers(5)
        for m in matchers:
            asserts.equal(m, m)
            assert not m != m
        asserts.equal(set((m.Interest for m in matchers)), {Interest})
        asserts.equal(set((m.Interest.Map for m in matchers)), {Interest.Map})
        asserts.equal(set((m.Event for m in matchers)), {Event})
        asserts.equal(set((m.Subscription for m in matchers)), {Subscription})
