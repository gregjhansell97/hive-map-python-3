========
OUT OF DATE (WILL BE UPDATED SOON) Hive-Map
========

Communication Agnostic Distributed Pub-Sub Network

Description
===========

For a longer description go to hive-map's `homepage <https://github.com/gregjhansell97/hive-map>`_

Installation
============
- using python 3.7 or newer

.. code-block:: bash

    pip install -e .

Testing
=======
.. code-block:: bash

    python setup.py test

Auto-Document Code
========================
.. code-block:: bash

    python setup.py docs

Example
========
This example runs two processes. One processes has a location instance that prints out 
messages published to it. The other processes has a destination instance that publishes
information to the location. Both instances use a udp-socket to communicate. This example, and 
more like it, can be found `here <https://github.com/gregjhansell97/hive-map>`_.

**In one process:**

.. code-block:: python

    from hmap import Location
    from hmap.sockets import UdpSocket

    # create a location instance: printers location id is 3
    printer = Location(3)
    
    # create a socket so the location instance can communicate
    s = UdpSocket("localhost:8080", neighbors=["localhost:9090"])
    printer.use(s)
    
    # subscribe a callback that handles the received messages
    printer.subscribe(lambda msg: print(msg))
    
    # blocking call that listens for messages over udp
    s.listen()

**In another process on the same computer:**

.. code-block:: python
    
    from hmap import Destination
    from hmap.sockets import UdpSocket
    
    # create a destination instance
    printer = Destination(3) # '3' targets printers location id
    
    # create a socket so the destination instance can communicate
    s = UdpSocket("localhost:9090", neighbors=["localhost:8080"])
    printer.use(s)
    
    # creates a background thread that listens on the socket
    s.listen(block=False)
    
    # publishes raw bytes to the printer destination
    for i in range(10):
        printer.publish(b"hello world")

Note
====

This project has been set up using PyScaffold 3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
