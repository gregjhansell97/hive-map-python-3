#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue
from threading import Lock
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
    def start(self):
        self.__start = time.time()
    @property
    def time(self):
        # busy wait
        while self.__start is None:
            pass
        return (time.time() - self.__start)*self.__speed
    def sleep(self, duration):
        # busy wait
        while self.__start is None:
            pass
        time.sleep(duration/self.__speed)
