#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Router:
    """Base class responsible for delivering published messages to the 
    appropriate subscribers. This base class delivers published events local to 
    the router to subscriptions on the router.
    """

    def __init__(self, *, matcher):
        """
        Args:
            matching: algorithm used for event and subscription creation
        """
        super().__init__()
        if not self.is_valid_matcher(matcher):
            raise ValueError("Invalid matching algorithm")
        self.__matcher = matcher
    @property
    def matcher(self):
        """Algorithm used for event and subscription creation"""
        return self.__matcher

    @property
    def network(self):
        # check if none raise value error
        # weak reference too
        return self.__network

    def start(self, network):
        """
        """
        # assign network variable
        pass

    def on_publish(self, event):
        """Invoked when publish occurs local to the router

        Args:
            event: local event
        """
        pass

    def on_router_publish(self, event):
        """
        """
        pass

    def is_valid_matching(self, algo):
        """Determines if matching algorithm can be used in routing protocol"""
        # TODO check to make sure it's a subclass of Matching
        return True
