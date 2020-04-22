#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.testing import asserts
from hmap.testing.fixtures import FHMap, fixture_test

from hmap.interface.communication import poll, poll_recv, poll_send

class FPollable(FHMap):
    @fixture_test
    def pollable(self):
        comms = self.connected()
        asserts.true(poll_send(comms))
        asserts.true(poll(comms))
        comms[0].send(b"msg1")
        asserts.true(poll_recv(comms, timeout=self.timeout))
        asserts.true(poll(comms))
        for c in comms:
            if c is not comms[0]:
                asserts.equal(c.recv(timeout=self.timeout), b"msg1")
            asserts.equal(c.recv(timeout=0), b"")
        # should be nothing left to poll
        asserts.false(poll_recv(comms, timeout=self.timeout))
        # close a comm, should get something
        comms[0].close()
        asserts.true(poll_recv(comms, timeout=self.timeout))
        asserts.true(poll_send(comms, timeout=self.timeout))
        asserts.true(poll(comms, timeout=self.timeout))
