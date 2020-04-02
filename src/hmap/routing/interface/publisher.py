#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.manet.interface.component import Component

class Publisher(Component):
    """Responsible for publishing information using transceivers provided"""

    def publish(self, *args, **kwargs):
        """Publish data of a certain topic

        Args:
            topic: topic to publish data to
            data: information being published
        """
        # pre-operations before algorithm defined publish
        # maybe through in thread-pool
        # IDEA: callbacks can either be coroutines or functions
        # for now they're just functions
        # a way to make the event unique
        e = self.context.Event(*args, **kwargs)
        raw_data = self.context.Event.serialize(e)
        
        # reconstruct raw_data with more headers
        raw_data = self.on_publish(raw_data, event=e)

        # sends to all receivers in context
        # maybe its better for context to have subscriptions...
        self.context.subscriptions.pursue(event)
        for rcv in self.context._receivers:
            rcv(self.context, raw_data, event=e)
        # transmits data on transceiver, do a try-catch
        try:
            self.transceiver.transmit(raw_data)
        except AttributeError:
            # transceiver was never set up properly
            pass

    def on_publish(self, raw_data, event=None):
        """Hook to publish message to manipulate what gets published, keep track
        of inheritance stack! Should not be sending data anywhere, the bytes
        returned are what gets transmitted

        Args:
            raw_data(bytes): bytes of data being published
            topic: topic being published (helpful hint)
            data: data being published

        Returns:
            (bytes): raw-bytes to publish
        """
        return raw_data

