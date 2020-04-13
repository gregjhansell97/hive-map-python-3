#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Network:
    def __init__(self, routers=[], matcher=None):
        if matcher is None:
            try:
                matcher = routers[0].matcher
            except IndexError:
                raise ValueError("specify matcher or routers")
        for r in routers:
            if r.matcher != matcher:
                raise TypeError("mismatch matchers")
        # privates classes
        self.__Interest = matcher.Interest
        self.__Event == matcher.Event
        self.__Sub == matcher.Subscription
        # private helpers 
        self.__matcher = matcher
        self.__subscriptions = self.__Interest.Map()
        self.__routers = routers
        for r in self.__routers:
            # TODO error handling machinery
            r.start(network)
    @property
    def interests(self):
        return self.__subscriptions.interests
    @property
    def matcher(self):
        return self.__matcher
    def publish(self, *args, **kwargs):
        e = self.__Event(*args, **kwargs)
        for s in self.__subscriptions.match(e):
            s.notify(e)
        for r in self.__routers:
            r.on_publish(e)
    def subscribe(self, *args, **kwargs):
        s = self.__Sub(*args, **kwargs)
        self.__subscriptions.add(s)
    def router_publish(self, router, event):
        for s in self.__subscriptions.match(e):
            s.notify(e)
        for r in self.__routers:
            if r is router:
                continue
            r.on_router_publish(e)
