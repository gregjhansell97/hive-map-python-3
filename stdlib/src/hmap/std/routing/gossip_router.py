#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid4
import random
from hmap.interface.routing import Router

class GossipRouter(Router):
    def __init__(
            *args, 
            transceivers=[], 
            stale_buffer_size=1000, 
            **kwargs):
        super().__init__(*args, **kwargs)
        self.__trxs = transceivers
    def close(self):
        for t in self.__trxs:
            t.close()
    def notify_router(self, event):
        serialize = self.Event.serialize
        raw_event = serialize(event)
        msg_id = struct.pack("I", random.getrandbits(32))
        msg = msg_id + raw_event
        for t in self.__trxs:
            t.transmit(msg)
