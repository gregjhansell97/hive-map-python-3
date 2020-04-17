#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import time

from hmap.interface import asserts
from hmap.interface.fixtures import FHMap, fixture_test

class FTransceiver(FHMap):
    @property
    def timeout(self): 
        return 0.3
    @property
    def instances(self):
        return self.connected_transceivers(10) + self.isolated_transceivers(10)

    @abstractmethod
    def connected_transceivers(self, n):
        """n Transceiver instances all in communication"""
        raise NotImplementedError

    @abstractmethod
    def isolated_transceivers(self, n):
        """n Transceiver instances not in communication with one another"""
        raise NotImplementedError

    @fixture_test
    def proper_close_operation(self):
        for t in self.instances:
            # for statement checks idempotency
            for i in range(3):
                t.close()
                try:
                    data = t.recv()
                except EOFError:
                    pass
                else:
                    raise AssertionError
    @fixture_test
    def connected_transmit_recv(self):
        transceivers = self.connected_transceivers(4)
        try:
            transceivers[0].transmit(b"msg1")
            for t in transceivers[1:]:
                asserts.equal(t.recv(timeout=self.timeout), b"msg1")
            # no more receives
            for t in transceivers:
                asserts.equal(t.recv(timeout=0), b"")
        finally:
            for t in transceivers:
                t.close()
        # close up shop:
        

    @fixture_test
    def isolated_transmit_recv(self):
        try:
            transceivers = self.isolated_transceivers(4)
            for t in transceivers:
                t.transmit(b"msg")
            time.sleep(self.timeout)
            for t in transceivers[1:]:
                asserts.equal(t.recv(timeout=0), b"")
        finally:
            for t in transceivers:
                t.close()
