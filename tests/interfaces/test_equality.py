#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

def test_is_equal_noequal_properties(FIEquality):
    instances = FIEquality.instances()
    for i in instances:
        for j in instances:
            if i is j:
                assert j is i
                assert i == j
                assert j == i
            if i == j:
                assert j == i
                assert not j != i
                assert not i != j
            if i != j:
                assert j != i
                assert not j == i
                assert not i == j
def test_equality(FIEquality):
    matches = FIEquality.matches()
    for i in matches:
        for j in matches:
            assert i == j
def test_inequality(FIEquality):
    mismatches = FIEquality.mismatches()
    for i in mismatches:
        ref_count = 0
        for j in mismatches:
            if i is j:
                ref_count += 1
            else:
                assert i != j, "mismatch should be not be equal"
        assert ref_count == 1, "each object should only appears once"
