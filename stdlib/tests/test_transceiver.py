#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pytest
import uuid

import time

#interface
from hmap.interface.communication.fixtures import FTransceiver
# standard library
from hmap.std.communication.transceivers import IPCTransceiver

class FIPCTransceiver(FTransceiver):
    @property
    def timeout(self):
        return 0.1
    def connected_transceivers(self, n):
        id_ = str(uuid.uuid4())
        trxs = [IPCTransceiver(id_) for _ in range(n)]
        # ensure transceivers functional ahead of time
        while True:
            trxs[0].transmit(b"recv")
            count = 0
            for t in trxs[1:]:
                if t.recv(timeout=self.timeout) == b"recv":
                    count += 1
            if count == len(trxs[1:]):
                return trxs
    def isolated_transceivers(self, n):
        return [IPCTransceiver(str(uuid.uuid4())) for _ in range(n)]

def test_ipc_transceiver():
    trx_fixture = FIPCTransceiver()
    trx_fixture.test()

