#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import math
import pytest
import random
import simpy
from threading import Thread, Lock
import time
import uuid

from hmap.interface.context.traits.orientation import X, Y
from hmap.interface.context.traits.temporal import Time, Sleep

from hmap.testing.communication.fixtures import FCommunicator
from hmap.testing.communication.traits.fixtures import FPollable
# simulation library
from hmap.sim.communication import LocalCommunicator
from hmap.sim.communication import RadioTransceiver

_logger = logging.getLogger(f"__name__")


class FLocalCommunicator(FCommunicator, FPollable):
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

class FRadioTransceiver(FCommunicator):
    class Context(X, Y, Time, Sleep):
        def __init__(self, x, y):
            self.__x = x
            self.__y = y
        @property
        def x(self):
            return self.__x
        @property
        def y(self):
            return self.__y
        @property
        def time(self):
            return time.time()
        def sleep(self, duration):
            return time.sleep(duration)
    def connected(self):
        world = str(uuid.uuid4())
        trxs = []
        for _ in range(20):
            x, y = (random.uniform(-1, 1), random.uniform(-1, 1))
            t = RadioTransceiver(
                context = self.Context(x, y),
                world = world,
                send_duration=0.1,
                recv_duration=0.01,
                send_range=5,
                recv_range=5,
                max_buffer_size=math.inf)
            trxs.append(t)
        time.sleep(1)
        return trxs
    def isolated(self, n):
        trxs = []
        for x, y in zip(range(n), range(n)):
            trxs.append(
                RadioTransceiver(
                    context = self.Context(x, y),
                    world = str(uuid.uuid4()),
                    send_duration=0.1,
                    recv_duration=0.01,
                    send_range=0.25,
                    recv_range=0.25,
                    max_buffer_size=math.inf))
        time.sleep(1)
        return trxs

def test_radio_transceiver(caplog):
    caplog.set_level(logging.INFO)
    comm_fixture = FRadioTransceiver()
    comm_fixture.test()


class Ctx(FRadioTransceiver.Context):
    def __init__(self, x, y, clock): 
        super().__init__(x, y)
        self.__clk = clock
    @property
    def time(self): 
        return self.__clk.time
    def sleep(self, duration):
        self.__clk.sleep(duration)


class ManualClock():
    def __init__(self):
        self.__env = simpy.Environment()
    @property
    def time(self):
        return self.__env.now
    def sleep(self, duration):
        l = Lock()
        l.acquire() # prevents lock from being acquired again
        t = self.__env.timeout(duration)
        t.callbacks.append(lambda t: l.release())
        with l: # acquite lock once its released on callback
            return 
    def tick(self, delay=0.1):
        env = self.__env
        time.sleep(delay)
        env.step()
        # go through all events of the same time
        now = env.now
        while now == self.__env.peek():
            self.__env.step()

def _test_radio_interference(caplog):
    caplog.set_level(logging.INFO)
    clock = ManualClock()
    trx0 = RadioTransceiver(
            context = Ctx(0, 0, clock),
            send_duration=1,
            recv_duration=1,
            send_range=1.5,
            recv_range=1.5,
            max_buffer_size=math.inf)
    trx2 = RadioTransceiver(
            context = Ctx(2, 0, clock),
            send_duration=1,
            recv_duration=1,
            send_range=1.5,
            recv_range=1.5,
            max_buffer_size=math.inf)
    trx4 = RadioTransceiver(
            context = Ctx(4, 0, clock),
            send_duration=1,
            recv_duration=1,
            send_range=1.5,
            recv_range=1.5,
            max_buffer_size=math.inf)
    world = [trx0, trx2, trx4]
    trx0.world = world
    trx2.world = world
    trx4.world = world

    def send(trx, data):
        Thread(target=trx.send, args=[data], daemon=True).start()

    def tick(clk):
        Thread(target=clk.tick, daemon=True).start()

    def recv(trx, expected, timeout=0):
        def assert_recv():
            assert trx.recv(timeout=timeout) == expected
        Thread(target=assert_recv, daemon=True).start()

    send(trx0, b"msg1")
    send(trx4, b"msg2")
    assert clock.time == 0
    clock.tick()
    assert clock.time == 1
    recv(trx2, b"", timeout=0)
    clock.tick()
    send(trx0, b"msg3")
    clock.tick()
    recv(trx2, b"msg3")
    clock.tick()
    assert trx2.interference_log == [(0,1)]

def _test_local_communicator(caplog):
    caplog.set_level(logging.INFO)
    comm_fixture = FLocalCommunicator()
    comm_fixture.test()


