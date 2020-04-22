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
        world = []
        for _ in range(20):
            x, y = (random.uniform(-1, 1), random.uniform(-1, 1))
            t = RadioTransceiver(
                context = self.Context(x, y),
                send_duration=0.1,
                recv_duration=0.01,
                send_range=5,
                recv_range=5,
                max_buffer_size=math.inf)
            world.append(t)
        # connect all transceivers to the world created
        for t in world:
            t.world = world
        return world
    def isolated(self, n):
        world = []
        for x, y in zip(range(n), range(n)):
            world.append(
                RadioTransceiver(
                    context = self.Context(x, y),
                    send_duration=0.1,
                    recv_duration=0.01,
                    send_range=0.25,
                    recv_range=0.25,
                    max_buffer_size=math.inf))
        for t in world:
            t.world = world
        return world

def test_radio_transceiver(caplog):
    caplog.set_level(logging.INFO)
    comm_fixture = FRadioTransceiver()
    comm_fixture.test()


"""
class ______ManualClock(FRadioTransceiver.Context):
    def __init__(self):
        self.__time = 0
        self.__pending = {}
        self.__pending_lock = Lock()
    @property
    def time(self):
        return self.__time
    @time.setter
    def time(self, t):
        assert t > self.__time # not time travelling
        self.__time = t
        # go through and notify pending times 
        with self.__pending_lock:
            while self.__pending != []
                pending_time, pending_condition = self.__pending[0]
                if t >= pending_time: # past pending, notify pending condition
                    pending_condition.notify_all()
                    self.__pending.pop(0)
                else: # t not yet at pending time
                    break
    def tick(duration):
        cv = None
        with self.__pending_lock:
            t = self.__time + duration
            for i in range(len(self.__pending)):
                pending_time, pending_condition = self.__pending[i]
                #       t
                #  p0
                if t > pending_time:
                    continue
                #        t
                #  p0    p1     p2
                elif t == pending_time:
                    cv = pending_condition.wait()
                #            t
                #   p0   p1     p2
                else: # t is before the next pending time
                    cv = Condition()
                    self.__pending.insert(i, (t, cv))
            if cv is None: # could not find a place to insert it
                cv = Condition()
                self.__pending.append((t, cv))
        cv.wait() # wait for condition to be met
"""
class ManualClock(FRadioTransceiver.Context):
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
        

def test_radio_transceiver_properties(caplog):
    caplog.set_level(logging.INFO)
    def print_time(clock, delay):
        print(f"{delay}: {clock.time}")
        clock.sleep(delay)
        print(f"{delay}: {clock.time}")

    c = ManualClock()
    t1 = Thread(target=print_time, args=([c, 5]))
    t1.start()
    t2 = Thread(target=print_time, args=([c, 3]))
    t2.start()
    t3 = Thread(target=print_time, args=([c, 1]))
    t3.start()

    c.tick(delay=5)
    t4 = Thread(target=print_time, args=([c, 2]))
    t4.start()

    c.tick()
    c.tick()





def test_local_communicator(caplog):
    caplog.set_level(logging.INFO)
    comm_fixture = FLocalCommunicator()
    comm_fixture.test()


