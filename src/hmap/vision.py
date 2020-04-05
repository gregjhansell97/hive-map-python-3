from hmap import Router
from hmap.matching import TopicBased
from some_module import GossipRouter

# don't need context for base router
def on_simple(topic, msg):
    print((topic, msg))
r = Router(
        matching=TopicBased("FlatInteger", "PyObj"))
r.subscribe(1, on_simple)
r.publish(1, ("hello world", 1, 2, 3))


# may need context
from hmap.context.properties import LocationInterface, BatteryLevelInterface \
        ZMQInterface

class MyContext(
        ZMQInterface,
        LocationInterface,
        PowerLevelInterface):
    pass # you may need to define initial locations for some of you

ctx = MyContext(loc=(1, 2))

# some algorithms may not need a context
router = HintRouter(
        context=MyContext
        matching=TopicBased("FlatInteger", "Bytes")a)
router = GossipRouter(
        context=ctx,
        matching=TopicBased("StringHierarchy", "PyObj"),
        probability=0.5)

router.publish("weather.vt.killington", (45, "*F"))
router.subscribe("weather.vt.killington", on_killington_weather)









