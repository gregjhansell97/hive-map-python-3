#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
context = ...
communicators = ...
matcher = ...
router = ...
node = Node(router)
"""



class Node:
    def __init__(self, router):
        self.__Event = router.matcher.Event
        self.__Sub = router.matcher.Subscription
        self.__router = router
    def publish(self, *args, **kwargs):
        e = self.__Event(*args, **kwargs)
        self.__router.notify(e)
    def subscribe(self, *args, **kwargs):
        s = self.__Sub(*args, **kwargs)
        self.__router.subscribe(s)
        return s
    def unsubscribe(self, s):
        self.__router.unsubscribe(s)
    def close(self):
        self.__router.close()
