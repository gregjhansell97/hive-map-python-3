from hmap.manet.interface import Publisher, Subscriber, Router

from hmap.routing.manet import Context # context for manet protocols
from hmap.routing.manet.protocols import Flood # flooding protocol (provide Standard)
from hmap.comm.transceivers import IPCTransceiver GlobTransceiver
from hmap.matching.Topic

# transceivers can have different tags to indicate level of comprehension
# transceivers have: broadcast, deliver, transmit, on_receive

ctx = Context(protocol=Flood, ontology=StringHierarchy, serializer=PySerializer)

import hmap.manet as manet 
# that way you can put caviats on various transceivers
import hmap.manet.transceivers import IPCTransceiver 

# key-word arguments imply topic style algorithm
# raises value error
ctx = manet.Context(
        routing_protocol="manet.Flood", 
        message_type="PyObj",
        topic_type="StringHierarchy",
        supported=["location", "velocity"] )

# those are two ways of doing it
ctx.Subscription
ctx.Event




# transceiver is context specific
#trx = IPCTransceiver("communication-channel") 

# transceiver links up to first context that it sees
#pub = ctx.Publisher() # manet.Publisher
#pub.transceiver = trx # raises error if trx is connected to other context
#pub.publish("weather.vt.killington", (1, 2, 3, "message"))

#sub = ctx.Subscriber()
#sub.transceiver = trx
#def on_killington_weather(topic, message):
#    pass
#sub.subscribe("weather.vt.killington", on_killington_weather)

# router could be doing background work... (all can be...)
#router = ctx.Router()
#router.transceiver = trx

# different protocols may have varying levels of inter-language ability

router = ctx.Router(heartbeat=0.0)
router.transceiver = trx
# router.receiver = trx
# router.transmitter = trx

router.subscribe("weather.vt.killington", on_killington_weather)
router.publish("weather.vt.killington", (45, "*F"))



from hmap.context import Context
from hmap.matching import TopicBased
from some_module import GossipRouter

ctx = Context()

# some algorithms may not need a context
router = GossipRouter(
        context=ctx,
        matching_protocol=TopicBased("StringHierarchy", "PyObj"),
        probability=0.5)

router.publish("weather.vt.killington", (45, "*F"))
router.subscribe("weather.vt.killington", on_killington_weather)









