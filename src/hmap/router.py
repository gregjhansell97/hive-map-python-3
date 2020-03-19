#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO:
# - fill out interface
# - document
# - implementation (pub-sub impl?)

from hmap.transceiver import Transceiver
from hmap.message import Message, PUB, ACK


class Router:
    """
    Responsible for forwarding messages received by publisher to other
    subscribers and routers

    Algorithm:
        Current algorithm floods the network with message, there is no feedback
        and message drops are not handled
    """

    def __init__(self):
        self._trxs = []
        self._stale_ids = []

    def use(self, trx: Transceiver):
        """
        Provide access to a transceiver that the subscriber can use to disperse
        and receive information about topics and routers

        Args:
            trx: transceiver publs
        """
        trx._subscribe(self._on_recv)
        self._trxs.append(trx)

    def _on_recv(self, trx: Transceiver, data: bytes):
        """
        """
        msg_type, header, body = Message.deserialize(data)
        if msg_type == PUB:
            msg_id, msg_topic = header
            if msg_id in self._stale_ids:
                # remove id (will add to front in the next few lines)
                self._stale_ids.remove(msg_id)
            # add message id to the front
            self._stale_ids.insert(0, msg_id)
            self._stale_ids = self._stale_ids[:50]
            # send to all channels
            for t in self._trxs:
                t.transmit(data)

