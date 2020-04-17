import hmap
from hmap import Router
from hmap.matching import topic_based
from some_module import GossipRouter

# don't need context for base router
def on_simple(topic, msg):
    print((topic, msg))
r = Router(
        matcher=topic_based.Matcher("FlatInteger", "PyObj"))
r.subscribe(1, on_simple)
r.publish(1, ("hello world", 1, 2, 3))


# may need context
from hmap.capabilities import Loc, BatteryLevel, Zmq

class MyCapabilitiy(ILoc, IBatteryLevel, IZmq)
    pass # you may need to define initial locations for some of you

ctx = MyContext(loc=(1, 2))

from hmap.communication.client_server import ZmqClient

single_server_router = SingleServerRouter(
        password = "wilkommen",
        matcher = topic_based.Matcher("FlatInt", "PyObj"))
single_server_router.client = ZmqClient("ipc:///tmp/server123")

hnet = hmap.Network([single_server_router])

hnet.publish("hello world")

# some algorithms may not need a context
hint_router = HintRouter(
        context=MyContext
        matcher=topic_based.Matcher("FlatInt", "Bytes"))
gossip_router = GossipRouter(
        context=ctx,
        matcher=topic_based.Matcher("StringHierarchy", "PyObj"),
        probability=0.5)

# create an entry-point into the network (supply routers too)
hnet = hmap.Network([hint_router, gossip_router])

hnet.publish("weather.vt.killington", (45, "*F"))
hnet.subscribe("weather.vt.killington", on_killington_weather)









