#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

def test_set_add(FIHash):
    matches = FIHash.matches()
    mismatches = FIHash.mismatches()
    assert len(set(matches)) == 1
    assert len(set(mismatches)) == len(mismatches)

def test_set_remove(FIHash):
    matches = FIHash.matches()
    mismatches = FIHash.mismatches()

    matches_set = set(matches)
    for m in matches:
        matches_set.remove(m)
        assert len(matches_set) == 0
        matches_set = set(matches)

    mismatches_set = set(mismatches)
    for m in mismatches:
        prior_len = len(mismatches_set)
        mismatches_set.remove(m)
        assert len(mismatches_set) == prior_len - 1
        # should't be able to remove again
        with pytest.raises(KeyError):
            mismatches_set.remove(m)
        mismatches_set = set(mismatches)
