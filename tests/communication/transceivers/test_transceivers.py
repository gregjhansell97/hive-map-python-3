#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import time

from hmap.communication.transceivers.ipc import Transceiver as IPCTransceiver

def test_isolated_transceivers(FSimTransceiver):
    get_cb = FSimTransceiver.get_callback
    trxs = FSimTransceiver.isolated_transceivers(10)
    cbs_per_trx = 3 # callbacks per tranceiver
    callbacks = [get_cb() for _ in range(len(trxs)*cbs_per_trx)]
    barrier = FSimTransceiver.barrier
    # subscribe callbacks
    for cb, i in zip(callbacks, range(len(callbacks))):
        t = trxs[i%len(trxs)]
        t.subscribe(cb)
        t.subscribe(cb) # subscribe twice (see if it screws anything up)
    # try to transmit on every instance
    for t in trxs:
        t.transmit(b"no connections")
        t.transmit(b"hopefully not!")
    barrier(trxs)
    # logs should not have anything because every trx is isolated
    for cb in callbacks:
        assert cb.log == []
    # unsubscribe all callbacks
    for cb, i in zip(callbacks, range(len(callbacks))):
        t = trxs[i%len(trxs)]
        t.unsubscribe(cb)
        # check cb is removed
        with pytest.raises(ValueError):
            t.unsubscribe(cb)
    # transmit w/o errors and to no one!
    for t in trxs:
        t.transmit(b"no connections")
        t.transmit(b"hopefully not!")
    barrier(trxs)
    # no messages
    for cb in callbacks:
        assert cb.log == []

def test_connected_transceivers(FSimTransceiver):
    get_cb = FSimTransceiver.get_callback
    trxs = FSimTransceiver.connected_transceivers(10)
    cbs_per_trx = 3 # callbacks per tranceiver
    barrier = FSimTransceiver.barrier
    # subscribe callbacks
    callbacks = {}
    for t in trxs:
        callbacks[t] = [get_cb() for _ in range(cbs_per_trx)]
        for cb in callbacks[t]:
            t.subscribe(cb)
            t.subscribe(cb) # subscribe twice (see if it screws anything up)

    # try to transmit on every instance
    for t, i in zip(trxs, range(len(trxs))):
        t.transmit(f"{i}".encode())
    barrier(trxs)

    # check callbacks
    for t, i in zip(trxs, range(len(trxs))):
        expected_log = {
                (t, f"{j}".encode()) 
                for j in range(len(trxs)) if j != i}
        for cb in callbacks[t]:
            assert expected_log == set(cb.log)
            # NOTE clear log!
            cb.log = []
    # unsubscribe some callbacks (first and last)
    for t, cbs in callbacks.items():
        t.unsubscribe(cbs[0])
        t.unsubscribe(cbs[-1])
    #TODO need some barrier
    # retransmit!
    for t, i in zip(trxs, range(len(trxs))):
        t.transmit(f"{i}".encode())
    barrier(trxs)

    # check callbacks
    for t, i in zip(trxs, range(len(trxs))):
        expected_log = {
                (t, f"{j}".encode())
                for j in range(len(trxs)) if j != i}
        # check unsubscribed callbacks didn't get anything
        assert callbacks[t][0].log == []
        assert callbacks[t][-1].log == []
        # verify calback ones did
        for cb in callbacks[t][1:-1]: # cbs starting at 1 and up to last index
            assert expected_log == set(cb.log)
            # NOTE clear log!
            cb.log = []

def test_changing_connections(FLocalTransceiver):
    get_cb = FLocalTransceiver.get_callback
    trxs = FLocalTransceiver.connected_transceivers(10)
    barrier = FLocalTransceiver.barrier
    # subscribe one callback per transceiver
    callbacks = {t: get_cb() for t in trxs}
    for t, cb in callbacks.items():
        t.subscribe(cb)

    # partition into two smaller
    trxs1 = trxs[:len(trxs)//2]
    trxs2 = trxs[len(trxs)//2:]

    for t1 in trxs1:
        t1.connect(t1) # NOTE: just see if this screws anything up
        for t2 in trxs2:
            # connection is one-way
            t1.disconnect(t2)
            t2.disconnect(t1)

    # try to transmit on every instance on trx1
    for t, i in zip(trxs, range(len(trxs))):
        t.transmit(f"{i}".encode())
    barrier(trxs)

    # check callbacks for TRXS1
    for t, i in zip(trxs1, range(len(trxs1))):
        expected_log = {
                (t, f"{j}".encode())
                for j in range(len(trxs1)) if j != i}
        assert expected_log == set(callbacks[t].log)
        # NOTE clear log!
        callbacks[t].log = []

    # check callbacks for TRXS2
    offset = len(trxs)//2 # trx2 latter half of partition 
    rng2 = range(offset, offset + len(trxs2))
    for t, i in zip(trxs2, rng2):
        expected_log = {
                (t, f"{j}".encode())
                for j in rng2 if j != i}
        assert expected_log == set(callbacks[t].log)
        # NOTE clear log!
        callbacks[t].log = []
        


    

def test_simple_ipc_transceiver():
    t1 = IPCTransceiver("./.will-this-work")
    t1.start()
    try:
        assert t1.leader
    except Exception as e:
        t1.stop()
        raise e
    '''
    t1 = IPCTransceiver("./.test-simple-ipc")
    t2 = IPCTransceiver("./.test-simple-ipc")
    t1.start()
    t2.start()
    def callback(trx, data):
        callback.log.append(data)
    callback.log = []
    t1.transmit(b"hello")
    t2.subscribe(callback)
    time.sleep(1)
    assert callback.log == [b'hello']
    t1.stop()
    t2.stop()
    '''



