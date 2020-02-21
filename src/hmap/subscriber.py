#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.transceiver import Transceiver

class Subscriber:
    """
    Responsible for invoking callbacks when messages of a certain topic are
    received

    Algorithm:
        Current algorithm floods the network with message, there is no feedback
        and message drops are not handled
    """
    def __init__(self, topic: int, cb):
        """
        """
        self._topic = topic
        self._callback = cb
        self._trxs = []

    def use(self, trx: Transceiver):
        """
        """
        trx._subscribe(self._on_recv)
        self._trxs.append(trx)

    def _on_recv(self, trx: Transceiver, data: bytes):
        """
        Receivers are listening for published messages, so I am assuming that
        they likely have the capacity to respond back... so the messages they
        can receive are published messages for now, but I can imagine a world
        where heart beats from other subscribers are broadcasted, so they can
        hear those too, but maybe should ignore them... LET THE ROUTER WORRY
        ABOUT THAT.
        """
        raise NotImplementedError
