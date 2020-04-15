#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
from multiprocessing import Pipe, Process
from multiprocessing.connection import Client, Listener, wait
from threading import Thread, Lock
import time

import hmap.communication.transceivers.abc as abc


def session(address, trx):
    connections = [] # list of connections
    threads = []
    listener = None
    session.stop = False
    session.lock = Lock()
    def manage_client(client):
        while True:
            try:
                data = client.recv_bytes()
            except EOFError:
                print("client is closing nooooooo")
                with session.lock:
                    connections.remove(client)
                    # no more connections, poison process
                    print("connections are nothing noooooo")
                    session.stop = True
                    trojan_client = Client(address, family="AF_UNIX")
                    print("done with this thread, and process")
                return # exit the thread
            print(f"RECEIVED DATA {data}")
            for c in connections:
                if c is client:
                    # don't send a message back
                    continue
                print("GOT TO HERE")
                # just try to send to other connections 
                c.send_bytes(data)
    try:
        # gonna have problems with AF_UNIX on windows machines
        listener = Listener(address, family="AF_UNIX")
    except Exception as e:
        trx.send_bytes(b"0") # didn't work
        return # end process
    with listener:
        trx.send_bytes(b"1") # successfully created listener
        print("SERVER RUNNING SUCCESSFULLY")
        #NOTE do not use trx after this point
        # go through and create connections
        while True:
            # gotta accept at least one client
            c = listener.accept()
            print("ACCEPTED CLIENT!!")
            print(session.stop)
            if session.stop:
                # client warned me to stop
                return 
            connections.append(c)
            threads.append(
                    Thread(target=manage_client, args=((c,)), daemon=True))
            threads[-1].start()
session.poison_pill = False

class Transceiver(abc.Transceiver):
    def __init__(self, address):
        super().__init__()
        # pass in a pipe that ends it
        self.__address = address
        self.__active = False
        self.__lock = Lock()
        self.__session = None # loop that runs server
        self.__server = None # way to communicate with server
        self.__poison_pill, pp = Pipe()
        self.__receive_loop = Thread(
                target=self.receive_loop, args=((pp,)), daemon=True)
        atexit.register(self.stop)
        # go on ahead with or without connection
    def active(self):
        return self.__active
    def start(self): 
        with self.__lock:
            self.__active = True
            self.__spawn_server()
            self.__receive_loop.start()
    def __spawn_server(self):
        address = self.__address
        # start-up the session
        session_pipe, trx_pipe = Pipe()
        daemon = Process(
                target=session, args=((address, trx_pipe)))
        daemon.start()
        # wait for either session to fail or succeed
        success = (session_pipe.recv_bytes() == b"1")
        # if it failed some other process has created the session or! there is
        # some ipc file that is impedeing it...
        # close pipes
        trx_pipe.close()
        session_pipe.close()
        # create client
        self.__server = Client(address, family="AF_UNIX")
    def stop(self): 
        #TODO aquire lock
        time.sleep(1)
        if not self.__active:
            return 
        with self.__lock:
            self.__active = False
            # end receive loop by closing server
            self.__server.close()
            print("closed conneciton to server")
            self.__poison_pill.send_bytes(b"DEAD")
            #self.__receive_loop.join()
            print("done with thread")
    def transmit(self, data):
        self.__server.send_bytes(data)
    def receive_loop(self, poison_pill):
        while True:
            responses = wait([self.__server, poison_pill])
            if poison_pill in responses:
                return 
            # otherwise it must have been the server
            # NOTE if structure changes this is no longer valid
            try:
                data = self.__server.recv_bytes()
            except EOFError:
                print("END OF LINE ERROR!")
                # TODO need lock here
                # end of correspondence with server
                print(self.active)
                if not self.active: # shutting down
                    print("exiting")
                    return
                # still active attempt to respawn server
                with self.__lock:
                    self.__spawn_server()
                continue
            print(self)
            print(f"{self}:RECEIVING DATA: {data}")
            self.receive(data)
        
