#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict, deque
import math
import random
import struct

from hmap.loc.messages import LocHeader


class Destination:
    """
    Publisher class in the hive-map ecosystem. Destinations interested in the
    same location work together to get their published data delivered to the
    location
    """

    def __init__(
        self, target: int, reliability: float = 0.9, learning_rate: float = 0.1
    ):
        """
        Creates a destination instance

        Args:
            target: id of target location
            reliability: min acceptable reliability for publishing messages; the
                range is from 0 to 1
            learning_rate: rate which reliability changes with new information, 
                the range is from 0 to 1 where 0 means that new information does
                not change the reliability and 1 means the reliability does not
                depend on past information. 

        Raises:
            ValueError: when reliability or learning_rate are not values
                between 0 and 1
        """
        if reliability < 0 or reliability > 1:
            raise ValueError("reliability is not bounded between 0 and 1")
        elif learning_rate < 0 or learning_rate > 1:
            raise ValueError("learning_rate is not bounded between 0 and 1")
        self._target = target  # id target location
        self._sockets = set()  # sockets used by destination to communicate
        self._min_reliability = reliability
        self._learning_rate = learning_rate
        self._distance = math.inf
        self._reliability = 0.0
        # defaultdict of int keys and values of 2-tuple type
        # key: distance away
        # value: (<prob of success>, <decrement count>)
        self._distances_table = defaultdict(lambda: (0.0, 0))
        # prevents redundant messages (both sending and receiving)
        self._sent_msg_ids = deque(maxlen=10)
        self._rcvd_msg_ids = deque(maxlen=10)

    @property
    def target(self):
        """
        Target location of the destination: published messages try to be
        delivered to target location
        """
        return self._target

    @property
    def distance(self):
        """
        Closest number of hops away to target destination while still perserving
        reliability
        """
        return self._distance

    @property
    def reliability(self):
        """
        Probability message published at the current distance will be 
        successfully delivered to the target location
        """
        return self._reliability

    def use(self, socket):
        """
        Uses a provided socket to interact with a network. Use is not 
        one-to-one. A destination can use multiple sockets and a socket can be
        used by multiple destinations. A destination cannot use a socket more
        than once

        Args:
            socket(hmap.network.AbstractSocket): socket used by destination to 
                reach out to other destinations and locations on a network

        Raises:
            ValueError: attempting to use socket more than once
        """
        if socket in self._sockets:
            raise ValueError
        socket._subscribe(self._target, self._deliver)
        self._sockets.add(socket)

    def publish(self, body: bytes):
        """
        Publishes raw bytes to the target location

        Args:
            body(bytes): raw bytes of message
        """
        # create a random message id and append it
        msg_id = random.randint(0, 0xFFFFFFFF)
        self._sent_msg_ids.append(msg_id)
        # look to publish body
        d = self.distance
        h = LocHeader(LocHeader.PUB, d, msg_id)
        raw_msg = LocHeader.serialize(h, body)
        # decrease reliability at distance (expectation that it will recv ack)
        self._decrement_reliability(d)
        for s in self._sockets:
            s._publish(self._target, raw_msg)

    def _deliver(self, socket, topic: int, data: bytes):
        """
        Handles logistics of data received by this destination

        Args:
            socket(hmap.network.AbstractSocket): socket invoking this _deliver
                method
            topic: topic of item deliverd (it should match target)
            data: data received by destination. Can receive a destiantion
                message that needs to be forwarded or receive an ack mesage that
                adjusts the reliabliity
        """
        # handles logistics of data received by a socket being used for a
        # specific destiantion
        assert topic == self._target
        # break apart data into a message
        h, b = LocHeader.deserialize(data)
        if h.type == LocHeader.PUB:  # publish message
            d = self.distance
            # filter out further distances and already received messages
            if d >= h.distance:
                return  # further away, can't do anything
            elif h.id in self._rcvd_msg_ids:
                return  # likely already received message
            # to do register h.id so that it can be ignored until refreshed
            self._rcvd_msg_ids.append(h.id)
            # publish ack
            self._publish_ack(d, h.id)
            ack_h = LocHeader(LocHeader.ACK, d, h.id)
            ack_b = struct.pack("B", round(self.reliability * 255))
            socket._publish(self._target, LocHeader.serialize(ack_h, ack_b))
            # forward information off
            self.publish(b)
        elif h.type == LocHeader.ACK:  # acknowledge message
            ack_distance = h.distance
            ack_prob = struct.unpack("B", b)[0] / 255
            if h.id in self._sent_msg_ids:  # likely a good ack
                self._increment_reliability(ack_distance + 1, ack_prob)

    def _decrement_reliability(self, distance):
        """
        Internal method that decreases reliability with the expectation that
        it will increase. Modifies _distances_table member. The _distance_table
        member modifies the distance and reliability properties

        Args:
            distance(int); distance from a neighboring node 
        """
        for d in sorted(self._distances_table.keys()):
            if d > distance:
                break
            p, c = self._distances_table[d]
            assert 1 >= p >= 0, "invalid probability"
            p *= 1 - self._learning_rate
            c += 1
            self._distances_table[d] = (p, c)
            if p < 0.01:
                del self._distances_table[d]
        self._refresh_distance_and_reliability()

    def _increment_reliability(self, distance, p_new):
        """
        Internal method that modifies _distances_table member based on new 
        information about a distance of a neighbor and its propability of 
        success. The _distance_table member modifies the distance and
        reliability properties

        Args:
            distance(int): distance from a neighboring node
            prob(float): probability message will be successfully delivered
                bounded by [0, 1]
        """
        p, c = self._distances_table[distance]
        c = 0 if p == 0 else c
        p_new = p_new
        delta = self._learning_rate
        if c > 0:
            c -= 1
            p_new = p + delta * (p_new) * ((1 - delta) ** (c))
        else:
            p_new = p + delta * p_new * (1 - p)
        self._distances_table[distance] = (p_new, c)
        self._refresh_distance_and_reliability()

    def _refresh_distance_and_reliability(self):
        """
        Updates _distance and _reliability based on _distances_table
        """
        prob_failure = 1.0
        # go from closest distance to furthest until accrued enough probability
        for d in sorted(self._distances_table.keys()):
            prob_failure *= 1 - self._distances_table[d][0]
            if 1 - prob_failure > self._min_reliability:
                self._distance = d
                self._reliability = round(1.0 - prob_failure, 3)
                return
        # could not accrue enough probability
        self._distance = math.inf
        self._reliability = round(1.0 - prob_failure, 3)
