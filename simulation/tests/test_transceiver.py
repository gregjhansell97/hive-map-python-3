#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pytest
import uuid

from hmap.interface.communication.fixtures import FTransceiver
# simulation library
from hmap.sim.communication.transceivers import ConnectableTransceiver

_logger = logging.getLogger(f"__name__")


class FConnectableTransceiver(FTransceiver):
    def connected_transceivers(self, n):
        transceivers = self.isolated_transceivers(n)
        for t1 in transceivers:
            for t2 in transceivers:
                if t1 is t2:
                    continue
                t1.connect(t2)
        return transceivers
    def isolated_transceivers(self, n):
        return [ConnectableTransceiver() for _ in range(n)]

def test_connected_transceiver():
    trx_fixture = FConnectableTransceiver()
    trx_fixture.test()

