#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from queue import Queue
import weakref


from multiprocessing import Pipe
from multiprocessing.connection import wait
from threading import Lock, Thread

from hmap.interface import has_traits
from hmap.interface.communication import Communicator
from hmap.interface.context.traits.orientation import X, Y
from hmap.interface.context.traits.temporal import Time, Sleep

from hmap.sim.communication.local_communicator import LocalCommunicator



class RadioTransceiver(Communicator):
    def __init__(
            self, *, context,
            send_duration=0.5, 
            recv_duration=0.5,
            send_range=1,
            recv_range=1,
            max_buffer_size=2048):
        if not has_traits(context, [X, Y, Time, Sleep]):
            raise TypeError("context does not have correct traits")
        super().__init__()
        self.__ctx = context
        self.__world = []
        self.__closed = False
        self.__buffer_lock  = Lock()
        self.__buffer = []
        self.__mailbox = Queue()
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


    # receive until unable to ""
    def send(self, data, timeout=None):
        if self.__closed:
            raise EOFError
        # check if in the process of receiving something (if so delay the send)
        while (timeout is None or timeout >= 0) and not self.__closed:
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
                self.__ctx.sleep(delay)
                if timeout is not None:
                    timeout -= delay
                # need to loop back and verify window is still open
                # there is a chance for interference and could get bigger

        data = pickle.dumps((self.send_duration, data))
        # get neighbors that are close
        for n in self.__world:
            n = n()
            if n is None or n is self or n.__closed:
                continue
            if n.in_range(self):
                n.__mailbox.put(data)
        # pause for duration (can't send anything else 
        self.__ctx.sleep(self.send_duration)
        return True
    def in_range(self, t):
        max_distance = self.recv_range + t.send_range
        dx = self.__ctx.x - t.__ctx.x
        dy = self.__ctx.y - t.__ctx.y
        return dx**2 +  dy**2 <= max_distance**2
    def update_buffer(self):
        while True:
            raw_data = self.__ipc_trx.recv(timeout=0) 
            if raw_data == b"": # no more bytes to recv
                return
            if raw_data is None or self.__closed: # poison pill, end loop
                self.__mailbox.task_done()
                return 
            t = self.__ctx.time 
            duration, data = pickle.loads(raw_data)
            # go through buffer
            # add new data to buffer
            with self.__buffer_lock:
                # start, end, data
                self.__buffer.append((t, t + duration, data))
                # put it at the end and bubble it up the list 
                i = len(self.__buffer) - 1 # start at end
                while i >= 1: # go to front
                    s1, e1, data1 = self.__buffer[i]
                    s0, e0, data0 = self.__buffer[i - 1] # look one ahead
                    # s1----e1
                    #             s0------e0
                    if e1 <= s0: # data moves ahead in line
                        self.__buffer[i - 1] = self.__buffer[i]
                        self.__buffer[i] = (s0, e0, data0)
                    #           s1----------e1
                    # s0--------e0
                    elif e0 <= s1: # data doesn't move
                        break # exit loop
                    else: # not ahead or behind, must be intersecting
                        # interference!
                        self.__buffer[i - 1] = (
                            min(s0, s1), max(e0, e1), "INTERFERENCE")
                        self.__buffer.pop(i) # remove extra buffer
                        break
                    i -= 1
            self.__mailbox.task_done()
            # CREATES A BUFFER #########################################
    def recv(self, timeout=None):
        # iterate through until timeout or message received
        while (timeout is None or timeout >= 0) and (not self.__closed):
            # pre-recv-pause
            self.__ctx.sleep(self.recv_duration)
            with self.__buffer_lock:
                time = self.__ctx.time
                buffer_size = 0
                # check buffer for maximum buffer size
                for i in range(len(self.__buffer)):
                    s, e, data = self.__buffer[i]
                    if type(data) is str:
                        # warnings of strings should not be in buffer size calc
                        continue
                    if s <= time: # started already
                        buffer_size += len(data)
                        if buffer_size > self.max_buffer_size:
                            # past buffer size, no bytes can be received
                            self.__buffer[i] = (s, e, "BUFFER OVERFLOW")
                    else: # not available yet (and neither is the rest)
                        break
                    data = None
                # attempt to remove first 'usable' message
                while not self.__closed:
                    try:
                        s, e, data = self.__buffer[0]
                    except IndexError:
                        break
                    if time >= e: # message completely sent
                        self.__buffer.pop() # remove message
                        if data == "INTERFERENCE": # interference
                            print("FOUND INTERFERENCE")
                            self.interference_log.append((s, e))
                            continue
                        elif data == "BUFFER OVERFLOW": # buffer overflow
                            # TODO log buffer overflow
                            continue
                        else: # data received!
                            if self.__closed:
                                raise NotImplementedError
                            return data
                    else: # data not completely sent
                        break
                if timeout is not None:
                    timeout -= self.recv_duration
        if self.__closed:
            raise EOFError
        return b"" # no dice after timeout
    def close(self):
        try:
            self.__mailbox.put(None)
            self.__closed = True
        except AttributeError: # closed before started
            return

