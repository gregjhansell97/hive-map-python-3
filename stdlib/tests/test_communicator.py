#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pytest
import uuid

import time

#interface
from hmap.interface.communication.fixtures import FCommunicator
# standard library
from hmap.std.communication import IPCTransceiver

class FIPCTransceiver(FCommunicator):
    @property
    def timeout(self):
        return 0.1
    def pairs(self, n):
        trxs = []
        for _ in range(n): 
            uid = str(uuid.uuid4())
            t1 = IPCTransceiver(uid)
            t2 = IPCTransceiver(uid)
            t1.send(b"hello")
            t2.recv()
            trxs.append((t1, t2))
        return trxs
    def isolated(self, n): 
        return [IPCTransceiver(str(uuid.uuid4())) for _ in range(n)]

def test_ipc_transceiver():
    trx_fixture = FIPCTransceiver()
    trx_fixture.test()

