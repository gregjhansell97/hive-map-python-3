#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interfaces that can be implemented by a subclasses. Used throughout
hive-map to verify the capability of an object
"""

import sched
import time

from abc import ABC, abstractmethod

# TODO: initial heartbeat is 0.0, heartbeat is cancelled when set to 0.0
class IHeartbeat(ABC):
    def __init__(self, *, max_heartbeat_rate):
        super().__init__()
        if heartbeat_rate < 0.0:
            raise ValueError("heartbeat rate must be positive")
        self.__max_hbeat = max_heartbeat_rate
        self.__hbeat = 0.0
        self.__hbeat_scheduler = None
        self.__cancel_loop = None
        # schedule item in initializer
        # TODO handle async heartbeat

        if heartbeat_rate > 0.0:
            self.__hbeat_scheduler = sched.scheduler(time.time, time.sleep)
            self.__cancel_loop = self.__hbeat_scheduler.enter(
                1.0 / self.__hbeat, 1, self.__hbeat_loop
            )

    def __hbeat_loop(self):
        # TODO: check if event already scheduled (prevent backing up)
        scheduler.enter(1.0 / self.__hbeat, 1, self.__hbeat_loop)
        # may run into some logging errors
        self.on_heartbeat()

    @property
    def heartbeat_rate(self):
        """Heartbeat rate used by router"""
        return self.__hbeat

    @heartbeat_rate.setter
    def heartbeat_rate(self, hbeat):
        if hbeat > self.__max_hbeat:
            raise ValueError("heartbeat rate too fast")
        self.__hbeat = hbeat

    @abstractmethod
    def on_hearbeat(self):
        """Periodically invoked based on heartbeat parameter"""
        raise NotImplementedError
