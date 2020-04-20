#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pytest
import uuid

import time

#interface
from hmap.testing.communication.fixtures import FCommunicator
# standard library
from hmap.std.communication import IPCTransceiver

class FIPCTransceiver(FCommunicator):
    @property
    def timeout(self):
        return 0.1
    def connected(self):
        uid = str(uuid.uuid4())
        Trx = IPCTransceiver
        trxs = [Trx(uid) for _ in range(10)]
        t0 = trxs[0]
        t0.send(b"hello")
        # ensure all transceivers can communicate
        for t in trxs[1:]:
            while not t.poll_recv(timeout=self.timeout):
                t0.send(b"hello")
        # drain t's of messages
        for t in trxs:
            while t.recv(timeout=0) != b"":
                continue
        return trxs

    def isolated(self, n): 
        return [IPCTransceiver(str(uuid.uuid4())) for _ in range(n)]

def test_ipc_transceiver(caplog):
    caplog.set_level(logging.INFO)
    trx_fixture = FIPCTransceiver()
    trx_fixture.test()
    time.sleep(1) # need time to shut everything down

