#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Facilitates publishing of topics. Publisher part of framework for the
pub-sub paradigm of hive-map

IDEAS/QUESTIONS:
- should a publisher be able to receive messages
* (2/23/20): I don't think they should because a publisher is going to be the
    weakest link in the network with the most SWaP dependence so it should do
    as little as possible. There would be some benefits to publisher having
    back-and-forth communication with routers/subscribers such as error
    detection; in a way that goes against the pub-sub paradigm. If a publisher
    publishes something, it shouldn't are what is listening. 
* (2/23/20): To consider failurs: what if there ar eno subscribers? message-id
    conflicts? matching message id from othe rmessages? no acks received? other
    messages publishing (don't flood network...)
* (2/23/20): What if nodes look for surounding nodes to find an identity, like
    a local (neighboring) agreement on a unique id...
* (2/23/20): I want to leave the routing to the routing nodes, I think it's 
    their responsibility... the publisher should be a lazy (low power) as
    possible
"""

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
        """
        Provide access to a transceiver that the publisher can use to disperse
        its information

        Args:
            trx: transceiver publs
        """
        self._trxs.append(trx)

    def publish(self, data: bytes):
        """
        Publish raw data to a topic, ideally subscribers of the topic receive
        this data

        Args:
            data: raw data being published
        """
        # need a message id (do not worry about ttl yet...)
        msg_type = PUB
        header = (random.randint(0, 65535),)
        msg = Message.serialize(msg_type, header, data)
