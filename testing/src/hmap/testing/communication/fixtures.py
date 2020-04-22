#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from threading import Thread
import time

from hmap.testing import asserts
from hmap.testing.fixtures import FHMap, fixture_test

class FCommunicator(FHMap):
    @property
    def timeout(self): 
        return 0.3
    @property
    def instances(self):
        instances = self.isolated(5)
        for c in self.connected():
            instances.append(c)
        return instances
    @abstractmethod
    def connected(self):
        """List of 2 or more communicator capable of directly receiving and
        transmitting data to one another 
        """
        raise NotImplementedError
    @abstractmethod
    def isolated(self, n):
        """n communicators where each communicator cannot communicate with
        anyone else
        """
        raise NotImplementedError

    @fixture_test
    def proper_close_operation(self):
        for c in self.instances:
            # for statement checks idempotency
            for _ in range(3):
                c.close()
                with asserts.raises(EOFError):
                    data = c.recv()
                with asserts.raises(EOFError):
                    c.send(b"still gonna send it!")
    @fixture_test
    def send_recv(self):
        comm1, *comms = self.connected()
        comm1.send(b"msg1")
        for c in comms:
            asserts.equal(c.recv(timeout=self.timeout), b"msg1")
        # no more receives
        for c in [comm1] + comms:
            asserts.equal(c.recv(timeout=0), b"")
        # close on a full stomach
        comm1.send(b"done")
        for c in [comm1] + comms:
            c.close()

    @fixture_test
    def spam_send_recv(self):
        comms = self.connected()
        for c in comms:
            c.send(b"msg")
        for c in comms:
            c.recv(timeout=0)

    @fixture_test
    def multi_threaded_spam_send_recv(self):
        def spam_send_recv(comms):
            # loop until comms are closed
            while True:
                for c in comms:
                    try:
                        c.send(b"msg")
                    except EOFError:
                        return
        comms = self.connected()
        t = Thread(target=spam_send_recv, args=(comms,))
        t.start()
        time.sleep(self.timeout)
        for i in range(10):
            for c in comms:
                c.recv(timeout=0)
        for c in comms: # turn thread off
            c.close()
        t.join()


    @fixture_test
    def isolated_send_recv(self):
        comms = self.isolated(4)
        for c in comms:
            c.send(b"msg")
        time.sleep(self.timeout)
        for c in comms:
            asserts.equal(c.recv(timeout=0), b"")

    @fixture_test
    def partial_close_send_recv(self):
        comm1, comm2, *comms = self.connected()
        comm2.close()
        comm1.send(b"msg1")
        with asserts.raises(EOFError):
            comm2.recv(timeout=self.timeout)
        for c in comms:
            asserts.equal(c.recv(timeout=self.timeout), b"msg1")

    @fixture_test
    def concurrent_close_and_recv(self):
        def recv_close(c):
            with asserts.raises(EOFError):
                c.recv(timeout=2)
        comm1, *comms = self.connected()
        t = Thread(target=recv_close, args=[comm1])
        t.start()
        comm1.close()
        t.join()
        
