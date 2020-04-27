#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue
from threading import Lock, Condition
import time

from hmap.interface.context.traits import temporal
import simpy

@dataclass(order=True)
class Item:
    priority: float
    item: Any=field(compare=False)

class Clock(temporal.Time, temporal.Sleep):
    def __init__(self, speed=1):
        self.__speed = speed # seconds per second
        self.__sleepers = PriorityQueue()
        self.__time = 0
        self.__start = None
        self.__starting = Condition()

    def start(self):
        with self.__starting:
            self.__start = time.time()
            self.__starting.notify_all()
    def _wait_for_start(self):
        if self.__start is None:
            with self.__starting:
                if self.__start is None:
                    self.__starting.wait()
    @property
    def time(self):
        self._wait_for_start()
        return (time.time() - self.__start)*self.__speed
    def sleep(self, duration):
        self._wait_for_start()
        time.sleep(duration/self.__speed)
