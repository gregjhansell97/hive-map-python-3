#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from threading import Thread, Lock


from hmap.interface.routing import Router
from hmap.interface import has_traits
from hmap.interface.context.traits import uid, random


class GossipRouter(Router):
    def __init__(
            self,
            *,
            matcher,
            context,
            transceiver,
            gossip_level=0.5):

        # verify correct context
        if not has_traits(context, [uid.Bytes, random.Uniform]):
            raise TypeError("context missing traits")
        super().__init__(matcher=matcher)
        
        self.__ctx = context
        self.__trx_lock = Lock()
        self.__trx = transceiver

        self.__gossip_level = gossip_level

        self.__router_table = {}
        self.__msg_count = 0

        self.__recv_loop_thread = Thread(target=self.recv_loop)
        self.__recv_loop_thread.start()
        

    def close(self):
        #TODO may want to join threads
        self.__trx.close()
        self.__recv_loop_thread.join()

    def recv_loop(self):
        while True:
            try:
                raw_data = self.__trx.recv()
            except EOFError: # file is closed
                return
            # extract data
            uid, mcount, b_event = pickle.loads(raw_data)
            # see if its relevant or new
            if uid == self.__ctx.uid:
                continue
            if (uid not in self.__router_table or 
                    mcount > self.__router_table[uid]):
                self.__router_table[uid] = mcount # most recent msg
                event = self.Event.deserialize(b_event)
                self.notify_subscriptions(event)
                # forward off the data to other neighbors if new
                if self.__ctx.random_uniform(0, 1) <= self.__gossip_level:
                    with self.__trx_lock:
                        try:
                            self.__trx.send(raw_data)
                        except EOFError:
                            return 
            else:
                pass
                #print(mcount)
                #print("SEEN IT BEFORE")


    def notify_router(self, event):
        uid = self.__ctx.uid
        mcount = self.__msg_count
        b_event = self.Event.serialize(event)

        raw_msg = pickle.dumps((uid, mcount, b_event))

        # send message off! 
        self.__msg_count += 1
        with self.__trx_lock:
            try:
                self.__trx.send(raw_msg)
            except EOFError:
                return 

