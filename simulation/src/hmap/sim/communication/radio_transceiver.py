#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import pickle
from queue import PriorityQueue
import weakref


from multiprocessing import Pipe
from multiprocessing.connection import wait
from threading import Lock, Thread

from hmap.interface import has_traits
from hmap.interface.communication import Communicator
from hmap.interface.context.traits.orientation import X, Y
from hmap.interface.context.traits.temporal import Time, Sleep
from hmap.std.communication import IPCTransceiver
from hmap.sim.communication.local_communicator import LocalCommunicator


def in_range(recv_loc, recv_range, send_loc, send_range):
    rx, ry = recv_loc
    sx, sy = send_loc
    max_distance = recv_range + send_range
    dx = rx - sx
    dy = ry - sy
    return dx**2 + dy**2 <= max_distance**2

class RadioTransceiver(Communicator):
    def __init__(
            self, *, context, world,
            send_duration=0.5, 
            recv_duration=0.5,
            send_range=1,
            recv_range=1,
            max_buffer_size=math.inf):
        if not has_traits(context, [X, Y, Time, Sleep]):
            raise TypeError("context does not have correct traits")
        self.__ipc_trx_lock = Lock()
        self.__ipc_trx = IPCTransceiver(world)
        super().__init__()
        self.__ctx = context
        self.__buffer_lock  = Lock()
        self.__buffer = []
        # public attributes
        self.send_duration = send_duration
        self.recv_duration = recv_duration
        self.send_range = send_range
        self.recv_range = recv_range
        self.max_buffer_size=max_buffer_size
        # stuff to log
        self.interference_log = []
        self.send_log = []
        self.recv_log = []

        self.__last_sent = -math.inf

    @property
    def loc(self):
        return (self.__ctx.x, self.__ctx.y)

    @property
    def time(self):
        return self.__ctx.time


    # receive until unable to ""
    def send(self, data, timeout=None):
        #print(f"{id(self)}: {self.loc}")
        # check if in the process of receiving something (if so delay the send)
        """
        while (timeout is None or timeout >= 0):
            self.update_buffer()
            t = self.__ctx.time # current time
            delay = None
            # search buffer for on going transmissions
            for s, e, data in self.__buffer:
                assert t >= s # can't travel to the past!!!
                #  t------------...
                #s---------e
                if t >= s and t < e: # in the middle of a transmission
                    delay = e - t # found a delay, want to wait until its done
                    break 
            if delay is None:
                break # all clear not receiving anything
            elif timeout is not None and timeout < delay:
                # not enough time to wait for a time window
                return False
            else: # enough time to sleep
                print("going to sleep")
                self.__ctx.sleep(delay)
                if timeout is not None:
                    timeout -= delay
                # need to loop back and verify window is still open
                # there is a chance for interference and could get bigger
        """
        # keeps from sending before ready
        while self.__ctx.time - self.__last_sent < self.send_duration:
            pass
        self.__last_sent = self.__ctx.time

        data = pickle.dumps(
                ((self.loc, 
                 (self.send_range, self.recv_range), 
                 self.send_duration, 
                 data)))
        assert(self.__ipc_trx.send(data))
        # get neighbors that are close
        #self.__ctx.sleep(self.send_duration)
        return True


    def update_buffer(self):
        while True:
            #with self.__ipc_trx_lock:
            raw_data = self.__ipc_trx.recv(timeout=0) 
            # FORMERLY LOCKED^^^^
            if raw_data == b"": # no more bytes to recv
                return

            # filter out messages out of range
            other_loc, other_comm_range, duration, data = pickle.loads(raw_data)
            other_send_range, _ = other_comm_range
            if not in_range(
                self.loc, self.recv_range, 
                other_loc, other_send_range):
                continue # message is out of range (not interesting)

            # go through buffer
            # add new data to buffer
            t = self.__ctx.time 
            #FORMERLY LOCKED
            #with self.__buffer_lock:
                # start, end, data
            self.__buffer.append((
                t, t + duration, 
                other_loc, other_comm_range, 
                data))
            # put it at the end and bubble it up the list 
            i = len(self.__buffer) - 1 # start at end
            while i >= 1: # go to front
                s1, e1, loc1, comm1, data1 = self.__buffer[i]
                s0, e0, loc0, comm0, data0 = self.__buffer[i - 1] # look one ahead
                # s1----e1
                #             s0------e0
                if e1 <= s0: # data moves ahead in line
                    self.__buffer[i - 1] = self.__buffer[i]
                    self.__buffer[i] = (s0, e0, loc0, comm0, data0)
                #           s1----------e1
                # s0--------e0
                elif e0 <= s1: # data doesn't move
                    break # exit loop
                else: # not ahead or behind, must be intersecting
                    # see if in range of each other
                    send_range, _ = comm0
                    _, recv_range = comm1
                    # loc1 could hear loc0
                    if in_range(loc1, recv_range, loc0, send_range): 
                        #print("##########################")
                        #print(f"{loc0}: {s0}-{e0}")
                        #print(f"{loc1}: {s1}-{e1}")
                        #print("##########################")
                        #print("COMPROMISE!")
                        # would have compromised
                        self.__buffer.pop(i) # remove faulty item and add
                        self.__buffer.append(
                                (e0, e0 + duration,
                                 loc1, comm1,
                                 data1))
                        i = len(self.__buffer) - 1 # restart!
                    else: # could not hear each other, interference!
                        self.__buffer[i - 1] = (
                                s0, e0, loc0, comm0, "INTERFERENCE")
                        self.__buffer[i] = (
                                s1, e1, loc1, comm1, "INTERFERENCE")
                        break
                i -= 1
            # FORMERLY LOCKED^^^^
    def recv(self, timeout=None):
        # iterate through until timeout or message received
        self.__ctx.sleep(self.recv_duration)
        while timeout is None or timeout >= 0:
            start_time = self.time
            self.update_buffer()
            # pre-recv-pause
            #FORMERLY LOCKED
            #with self.__buffer_lock:
            time = self.time
            buffer_size = 0
            # check buffer for maximum buffer size
            for i in range(len(self.__buffer)):
                s, e, loc, comm, data = self.__buffer[i]
                if type(data) is str:
                    # warnings of strings should not be in buffer size calc
                    continue
                if s <= time: # started already
                    buffer_size += len(data)
                    if buffer_size > self.max_buffer_size:
                        # past buffer size, no bytes can be received
                        self.__buffer[i] = (s, e, loc, comm, "BUFFER OVERFLOW")
                else: # not available yet (and neither is the rest)
                    break
                data = None
            # attempt to remove first 'usable' message
            while True:
                try:
                    s, e, loc, comm, data = self.__buffer[0]
                except IndexError:
                    break # not more messages!
                if time >= e: # message completely sent
                    self.__buffer.pop(0) # remove message
                    if data == "INTERFERENCE": # interference
                        #self.interference_log.append((s, e))
                        #print("INTERFERENCE :(")
                        continue
                    elif data == "BUFFER OVERFLOW": # buffer overflow
                        print("really shouldnt be here")
                        # TODO log buffer overflow
                        continue
                    else: # data received!
                        return data
                else: # data not completely sent
                    break
            if timeout is not None:
                elapsed_time = self.time - start_time
                timeout -= elapsed_time
            # FORMERLY LOCKED
        return b"" # no dice after timeout
    def close(self):
        self.__ipc_trx.close()

