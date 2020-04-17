#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid4
from hmap.interface.routing import Router

class GossipRouter(Router):
    def __init__(
            *args, 
            transceivers=[], 
            uid=uuid4(), 
            stale_buffer_size=1000, 
            **kwargs):
        super().__init__(*args, **kwargs)
        self._trxs = transceivers
        self._timestamp = 0
    def close(self):
        for t in self._trxs:
            t.close()
    def notify_router(self, event):
        serialize = type(event).serialize
        raw_event = serialize(event)
        msg_id = uid + struct.pack("I", self._timestamp)
        pass
