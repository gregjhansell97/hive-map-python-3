#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Facilitates receiving published messages of a certain topic. Subscriber part
of pub-sub paradigm of hive-map
"""

from hmap.transceiver import Transceiver
from hmap.message import Message, PUB, ACK


class Subscriber:
    """
    Responsible for invoking callbacks when messages of a certain topic are
    received

    Algorithm:
        Current algorithm floods the network with message, there is no feedback
        and message drops are not handled
    """

    def __init__(self, topic: int, cb):
        self._topic = topic
        self._callback = cb
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
        Receivers are listening for published messages, so I am assuming that
        they likely have the capacity to respond back... so the messages they
        can receive are published messages for now, but I can imagine a world
        where heart beats from other subscribers are broadcasted, so they can
        hear those too, but maybe should ignore them... LET THE ROUTER WORRY
        ABOUT THAT. If it hears an ack from a subscriber but it didn't hear that
        item them it could raise some sort of earro or ask for the information
        """
        msg_type, header, body = Message.deserialize(data)
        if msg_type == PUB:
            msg_id, msg_topic = header
            if msg_id in self._stale_ids:
                # remove id (will add to front in the next few lines)
                self._stale_ids.remove(msg_id)
            elif self._topic == msg_topic:
                self._callback(body)
            # add message id to the front
            self._stale_ids.insert(0, msg_id)
            self._stale_ids = self._stale_ids[:50]

