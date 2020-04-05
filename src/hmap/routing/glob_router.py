#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools

from routing.router import Router
import matching


class GlobRouter(Router):
    """Handles using multiple routers at once, encapsulates routers and behaves
    as one router. If events published on this router then event will be
    published on all of its routers. If an event is subscribed to this router
    then it will be notified of events any of the routers
    """

    def __init__(self, routers=[], matching=None):
        """
        Args:
            routers(object): iterable object that contains routers
            matching(matching.Algorithm): matching algo used for glob router
        """
        r_iter = iter(routers)
        if matching is None:
            self.matching = next(routers)
        for r in r_iter:
            if type(r.matching) is not type(self.matching):
                raise ValueError("all matching algorithms must be same type")
        super().init(matching=matching)
        self.__routers = routers

    @property
    def routers(self):
        """Mutable list of routers"""
        return self.__routers

    def on_publish(self, event):
        local_subs = self.subscriptions.matches(event)
        # go through local subscriptions first
        for s in local_subs:
            s.notify(event)

        # matching subscriptions from routers
        matching_subs = (r.subscriptions.matches(event) for r in self._routers)

        for s in itertools.chain(*r_subs):
            # ensure local subscriptions are not notified
            if s not in local_subs:
                s.notify(event)

    def on_subscribe(self, subscription):
        super().add(subscription)
        # NOTE: at this point subscription should be immutable
        for r in self._routers:
            self.on_subscribe(subscription)
