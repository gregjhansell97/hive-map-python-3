#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from hmap.transceiver import Transceiver
from hmap.message import Message, PUB

class Publisher:
    """
    Responsible for publishing information (to a specific topic) using 
    transceivers provided

    Algorithm:
        Current algorithm floods the network with message, there is no feedback
        and message drops are not handled
    """
    def __init__(self, topic: int):
        self._topic = topic
        self._trxs = []
        self._stale_ids = []

    def use(self, trx: Transceiver):
        self._trxs.append(trx)

    def publish(self, data:bytes):
        # need a message id (do not worry about ttl yet...)
        msg_type = PUB
        header = (random.randint(0, 65535),)
        msg = Message.serialize(msg_type, header, data)

    """
    def _receive(self, transceiver: Transceiver, raw_data: bytes):
        maybe all of these come down to the router nodes, like should a
        Publisher be as dumb as possible, and only have a range of 1 hop and
        then hope that it gets to a router
        Possible items to be received:
            errors:
                - you shouldn't care if publish has an error, all a publisher
                    is doing is its own thing and if someone wants to listen
                    by all means... its not the publishers job to worry about
                    that!
                failure to reach subscribers (what if there is no subscribers?)
                message-id conflict (potentially change name...)
                matching message id from other message
                no acks received (what is a good timeout for that...)
            other messages publishing, but as a publisher do you really
                care about other messages published... could result in flooding
                the network
            what if nodes that enter the network as the surrounding nodes for an
            identity and then they route messages based on given identities
            because it would be way more efficient if 
        # what to do here?
    """

