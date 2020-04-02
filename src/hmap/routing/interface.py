#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SCRATCH PAD:
    TODO:
        0. Life-cycle [100%]
        0.1 Method description
        1. link up to context [100%]
        1.1 link up receivers [100%]
        2. hearbeat thread [100%]

    Life-cycle:
    - creation: component is created
        - child constructor invokes super with arguments
        - launches heartbeat thread if rate is above 0.0 and on_heartbeat exists
        - connects to transceiver(weak reference)
        - connects to context(weak reference)
    - transceiver connection:
        - makes transceiver it's transceiver
        - subscribes itself to messages on transceiver if has on_recv
    - context connection:
        - makes context it's context
        - subscribes itself to messages on context ifhas on_recv
    - publish:
        - serializes message
        - provides hints like topic, and message to on_publish (if it exists)
    - destruction: publisher is destroyed
        - kills hearbeat thread
        - disconnects from transceiver
        - disconnects from context



"""

import sched
import time
import uuid

from todo import Transceiver

def supported_router_properties(*supported_props):
    """Class decorator that only keeps router properties specified as supported
    """
    # convert supported properties to a set
    supported_props = set(supported_props)
    props = inspect.getmembers(Router, lambda 0: isinstance(o, property))
    # convert to just string name of router properties
    props = {pname for pname, _ in props}
    # make sure supported properties exist
    if not supported_props.issubset(props):
        diff = list(supported_props.difference(props))
        raise AttributeError(f"{diff} router properties do not exist")
    # get properties that are not supported
    non_supported_props = props.difference(supported_properties)
    def decorator(cls):
        if not issubclass(cls, Router):
            raise ValueError("decorated class not subclass of Router")
        def raise_attribute_error(*args, **kwargs):
            raise AttributeError("attribute not supported")
        
        kwargs = {
                "fget": raise_attribute_error,
                "desc": "Not supported by router"
        }
        # go through non-supported props and override parent class
        for p in non_supported_props:
            # if you can't beat them... join them
            setattr(cls, p, property(**kwargs))

class Router:
    def __init__(self, *, matching_algorithm, context=None, heartbeat_rate=0.0):
        """
        Args:
            matching_algorithm: algorithm used for event and subscription 
                creation
            heartbeat_rate(float): on_heartbeat invocations per second
        """
        super().__init__()
        # confirm valid keyword arguments 
        if not self.is_valid_context(context):
            raise ValueError("invalid context")
        if not self.is_valid_matching_algorithm(matching_algorithm):
            raise ValueError("invalid matching algorithm")
        if heartbeat_rate < 0.0:
            raise ValueError("heartbeat rate must be positive")

        # private variables for attributes
        self.__ctx = context
        self.__trx = None # transceiver
        self.__matching_algo = matching_algorithm
        self.__subscriptions = matching_algorithm.Subscription()

        # private variables to support heartbeat
        self.__max_hbeat = heartbeat_rate
        self.__hbeat = heartbeat_rate
        self.__hbeat_scheduler = None

        # schedule item in initializer
        # TODO handle async heartbeat
        if heartbeat_rate > 0.0:
            self.__hbeat_scheduler = sched.scheduler(time.time, time.sleep)
            self.__cancel_loop = self.__hbeat_scheduler.enter(
                    1.0/self.__hbeat,
                    1,
                    self.__hbeat_loop)

    def __hbeat_loop(self):
        # TODO: check if event already scheduled (prevent backing up)
        scheduler.enter(1.0/self.__hbeat, 1, self.__hbeat_loop)
        # may run into some logging errors
        self.on_heartbeat()

    @property
    def subscriptions(self):
        return self.__subscriptions
    @property
    def matching_algorithm(self):
        """Algorithm used for event and subscription creation"""
        return self.__matching_algo
    @property
    def heartbeat_rate(self):
        """Heartbeat rate used by router"""
        return self.__hbeat
    @heartbeat_rate.setter
    def heartbeat_rate(self, hbeat):
        if hbeat > self.__max_hbeat:
            raise ValueError("heartbeat rate too fast")
        self.__hbeat = hbeat
    @property
    def context(self):
        """Cotext used by component"""
        return self.__ctx
    # COMMUNICATORS
    @property
    def transceiver(self):
        """Transceiver used to transmit and receive data"""
        return self.__trx
    @self.transceiver.setter
    def transceiver(self, trx):
        valid_trx = False
        for C in self.__supported_communication:
            if issubclass(trx.__class__, C):
                valid_trx = True
                break
        if not valid_trx:
            raise ValueError("incompatable transceiver")
        # check if already bound to transceiver
        if trx is self.__trx:
            return
        # unsubscribe old trx
        if self.__trx is not None:
            self.__trx.unsubscribe(self.on_transceiver_recv)
        # change transceiver
        self.trx = trx
        # add new receiver callback
        if self.__trx is not None:
            self.__trx.subscribe(self.on_transceiver_recv)

    def publish(self, *args, **kwargs):
        """Publishes an event
        
        Args:
            *args: arguments passed to matching algorithm's Event constructor
            **kwargs: keyword arguments passed to matching algorithm's Event
                constructor
        """
        e = self.__matching_algo.Event(*args, **kwargs)
        self.on_publish(e)

    def subscribe(self, *args, **kwargs):
        """Creates a subscription

        Args:
            *args: arguments passed to matching algorithm's Subscription 
                constructor
            **kwargs: keyword arguments passed to matching algorithm's 
                Subscription constructor
        """
        s = self.__matching_algo.Subscription(*args, **kwargs)
        self.on_subscription(s)
        return s

    def on_heartbeat(self):
        """Periodically invoked based on heartbeat parameter"""
        pass

    def on_publish(self, event):
        """Invoked when publish occurs locally

        Args:
            event: local event
        """
        self.__subscriptions.pursue(event)

    def on_subscription(self, subscription):
        """Invoked when subscription is created locally

        Args:
            subscription: local subscription
        """
        self.__subscriptions.add(subscription)

    def on_transceiver_recv(self, trx, raw_data): 
        """Callback for transceivers to invoke when new messages are received

        Args:
            trx(Transceiver): receiver of message
            raw_data(bytes): bytes received 
        """
        pass

    def is_valid_context(self, ctx):
        """Determines if context can be used in routing protocol"""
        return True


    def is_valid_matching_algorithm(self, algo):
        """Determines if matching algorithm can be used in routing protocol"""
        return True

