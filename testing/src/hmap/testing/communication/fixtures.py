#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from threading import Thread
import time

from hmap.testing import asserts
from hmap.testing.fixtures import FHMap, fixture_test

from hmap.interface.communication import poll, poll_recv, poll_send

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
            assert c.poll_recv(timeout=self.timeout)
            asserts.equal(c.recv(timeout=0), b"msg1")
        # no more receives
        for c in [comm1] + comms:
            asserts.equal(c.recv(timeout=0), b"")
        # close on a full stomach
        comm1.send(b"done")
        for c in [comm1] + comms:
            c.close()

    @fixture_test
    def isolated_send_recv(self):
        comms = self.isolated(4)
        for c in comms:
            c.send(b"msg")
        time.sleep(self.timeout)
        for c in comms:
            asserts.equal(c.recv(timeout=0), b"")

    @fixture_test
    def pollable(self):
        comms = self.connected()
        asserts.true(poll_send(comms))
        asserts.true(poll(comms))
        comms[0].send(b"msg1")
        asserts.true(poll_recv(comms, timeout=self.timeout))
        asserts.true(poll(comms))
        for c in comms:
            if c is not comms[0]:
                asserts.true(c.poll_recv())
                asserts.equal(c.recv(timeout=0), b"msg1")
            asserts.false(c.poll_recv())
        # should be nothing left to poll
        asserts.false(poll_recv(comms, timeout=self.timeout))
        # close a comm, should get something
        comms[0].close()
        asserts.true(poll_recv(comms, timeout=self.timeout))
        asserts.true(poll_send(comms, timeout=self.timeout))
        asserts.true(poll(comms, timeout=self.timeout))

    @fixture_test
    def partial_close_send_recv(self):
        comm1, comm2, *comms = self.connected()
        comm2.close()
        comm1.send(b"msg1")
        with asserts.raises(EOFError):
            comm2.recv(timeout=self.timeout)
        for c in comms:
            asserts.true(c.poll_recv(timeout=self.timeout))
            asserts.equal(c.recv(timeout=0), b"msg1")

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
        
