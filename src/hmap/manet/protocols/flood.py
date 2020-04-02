


class Flood(manet.interface.Protocol):
    """
    Have access to subscribers, publishers, and routers through context
    """
    def on_publish(self, publisher, raw_data):
        # do your thing with raw data
        raw_data = super().on_publish(self, publisher, raw_data)
        # TODO: add message-id to drop already seen messages
        return raw_data
    def on_router_recv(self, router, raw_data):
        # do your thing to the raw data
        # TODO: view message-id to drop already seen messages
        # that will transmit message to everywhere
        # pre processing
        # ability to peek at raw_data's topic?
        raw_data = super().on_router_recv(self, router, raw_data)
        # post processing
        return raw_data
    def on_subscriber_recv(self, subscriber, raw_data):
        # do your thing to the raw data
        return super().on_publish(self, publisher, raw_data)
