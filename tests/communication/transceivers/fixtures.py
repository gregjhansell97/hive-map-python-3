#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

from hmap.communication import Transceiver

from hmap.communication.transceivers.sim import LocalTransceiver

from tests.communication.fixtures import FCommunication

class FSimTransceiver(FCommunication):
    InstanceType = Transceiver
    @classmethod
    def get_callback(cls):
        def cb(trx, data):
            cb.log.append((trx, data))
        cb.log = []
        return cb
    @classmethod
    @abstractmethod
    def connected_transceivers(cls, num):
        raise NotImplementedError
    @classmethod
    @abstractmethod
    def isolated_transceivers(cls, num):
        raise NotImplementedError
    @classmethod
    def barrier(cls, trxs):
        pass # waits for all transceivers to be down dispatching

class FLocalTransceiver(FSimTransceiver):
    InstanceType = LocalTransceiver
    @classmethod
    @abstractmethod
    def instances(cls, num):
        return [cls.InstanceType() for _ in range(num)]
    @classmethod
    @abstractmethod
    def isolated_transceivers(cls, num):
        return cls.instances(num)
    @classmethod
    @abstractmethod
    def connected_transceivers(cls, num):
        instances = cls.isolated_transceivers(num)
        for i1 in instances:
            for i2 in instances:
                if i1 is not i2:
                    i1.connect(i2)
        return instances


base_fixtures = {FSimTransceiver}
impl_fixtures = {FLocalTransceiver}
