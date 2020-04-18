#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import time

from hmap.interface import asserts
from hmap.interface.fixtures import FHMap, fixture_test

class FCommunicator(FHMap):
    @property
    def timeout(self): 
        return 0.3
    @property
    def instances(self):
        instances = self.isolated(5)
        for p in self.pairs(2):
            instances.extend(p)
        return instances
    @abstractmethod
    def pairs(self, n):
        """n pairs of communicators where each pair can communicate with one
        another"""
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
                try:
                    data = c.recv()
                except EOFError:
                    pass
                else:
                    raise AssertionError
    @fixture_test
    def pair_send_recv(self):
        comm1, comm2 = self.pairs(1)[0]
        try:
            comm1.send(b"msg1")
            asserts.equal(comm2.recv(timeout=self.timeout), b"msg1")
            # no more receives
            asserts.equal(comm1.recv(timeout=0), b"")
            asserts.equal(comm2.recv(timeout=0), b"")
        finally:
        # close up shop:
            comm1.close()
            comm2.close()
        

    @fixture_test
    def isolated_send_recv(self):
        comms = self.isolated(4)
        try:
            for c in comms:
                c.send(b"msg")
            time.sleep(self.timeout)
            for c in comms:
                asserts.equal(c.recv(timeout=0), b"")
        finally:
            for c in comms:
                c.close()
