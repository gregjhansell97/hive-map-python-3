

from hmap import Publisher, Subscriber, Router

from hmap.transceivers import IPCTransceiver
from hmap.handlers import StringTopicHandler, PyMsgHandler

# idea of handlers:
# they deal with making sure the data is packed correctly for where ever it
# goes, it is the developers responsibility to make sure that messages have
# appropriate handlers


p = Publisher(message_handler=..., topic_handler=...)
t = IPCTransceiver("ipc:///communication-channel")
p.use(t)
p.message_handler = PyMsgHandler()
p.topic_handler = StringTopicHandler()

# last 
p.publish("weather.vt.killington", "yeet!")


p.publish("weather.vt.rutland", "yeet!")





from hmap.contexts import PyContext
from hmap.transceivers import IPCTransceiver


def on_killington_weather(msg): 
    pass

ctx = PyContext()
trx = IPCTransceiver("ipc:///communication-channel")
trx = InprocTransceiver()
trx.context = ctx 
trx.context = ctx

trx.publish("weather.vt.killington", "yeet!")
# returns subscriber object
trx.subscribe("weather.vt.killington", on_killington_weather)

r = Router(...)
r.transceiver= trx

# creates a router
ctx.Router(heartbeat_rate=0.01, topic_preference=)



from hmap.manet.interface import Publisher, Subscriber, Router

from hmap.manet import Context # context for manet protocols
from hmap.manet.protocols import flood # flooding protocol
from hmap.comm.transceivers import IPCTransceiver GlobTransceiver

# transceivers can have different tags to indicate level of comprehension
# transceivers have: broadcast, deliver, transmit, on_receive

ctx = Context(protocol=flood)
# transceiver is context specific
trx = IPCTransceiver("communication-channel") 

# transceiver links up to first context that it sees
pub = ctx.Publisher()
pub.transceiver = trx # raises error if trx is connected to other context
pub.publish(b"yeet", "weather.vt.killington")

sub = ctx.Subscriber()
sub.transceiver = trx
sub.subscribe(on_killington_weather, "weather.vt.killington")

# router could be doing background work... 
router = ctx.Router()
router.transceiver = trx

# different protocols may have varying levels of inter-language ability

