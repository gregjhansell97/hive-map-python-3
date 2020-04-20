#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pytest
import uuid

from hmap.testing.communication.fixtures import FCommunicator
# simulation library
from hmap.sim.communication import LocalCommunicator

_logger = logging.getLogger(f"__name__")


class FLocalCommunicator(FCommunicator):
    def connected(self):
        comms = self.isolated(5)
        for c1 in comms:
            for c2 in comms:
                if c1 is c2:
                    continue
                c1.connect(c2)
                c2.connect(c1)
        return comms
    def isolated(self, n):
        return [LocalCommunicator() for _ in range(n)]

def test_local_communicator(caplog):
    caplog.set_level(logging.INFO)
    comm_fixture = FLocalCommunicator()
    comm_fixture.test()

