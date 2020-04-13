#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pipe, Process
from multiprocessing.connection import Client, Listener, wait
from threading import Thread, Lock
import time

import hmap.communication.transceivers.abc as abc


def session(address, trx):
    connections = [] # list of connections
    threads = []
    def manage_client(client):
        while True:
            try:
                data = client.recv_bytes()
            except EOFError:
                # client is done
                connections.remove(client)
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
    try:
        trx.send_bytes(b"1") # successfully created listener
        print("SERVER RUNNING SUCCESSFULLY")
        #NOTE do not use trx after this point
        # go through and create connections
        while True:
            c = listener.accept()
            print("ACCEPTED LISTENER")
            connections.append(c)
            threads.append(Thread(target=manage_client, args=((c,))))
            threads[-1].start()
    except Exception as e:
        print("I GOT KILLED")
        listener.close()
        # close connections
        for c in connections:
            c.close()
        # join client threads
        for t in threads:
            t.join()
        raise e

class Transceiver(abc.Transceiver):
    def __init__(self, address):
        super().__init__()
        # pass in a pipe that ends it
        self.__address = address
        self.__active = False
        self.__lock = Lock()
        self.__session = None # loop that runs server
        self.__server = None # way to communicate with server
        self.__receive_loop = Thread(target=self.receive_loop)
        # go on ahead with or without connection
    @property
    def active(self):
        return self.__active
    @property
    def leader(self):
        return self.__session is not None
    def start(self): 
        with self.__lock:
            self.__active = True
            self.__spawn_server()
            self.__receive_loop.start()
    def __spawn_server(self):
        address = self.__address
        if self.leader:
            self.__session.kill()
            self.__session.join()
        # start-up the session
        session_pipe, trx_pipe = Pipe()
        self.__session = Process(target=session, args=((address, trx_pipe)))
        self.__session.start()
        # wait for either session to fail or succeed
        success = (session_pipe.recv_bytes() == b"1")
        if not success:
            self.__session.join()
            self.__session = None
        # close pipes
        trx_pipe.close()
        session_pipe.close()
        # create client
        self.__server = Client(address, family="AF_UNIX")
    def stop(self): 
        #TODO aquire lock
        with self.__lock:
            self.__active = False
            # end receive loop by closing server
            print("closing end of server")
            self.__server.close()
            self.__receive_loop.join()
            print("done with thread")
            # kill session if leader
            if self.leader:
                self.__session.kill()
                self.__session.join()
    def transmit(self, data):
        self.__server.send_bytes(data)
    def receive_loop(self):
        while True:
            try:
                data = self.__server.recv_bytes()
            except EOFError:
                # TODO need lock here
                # end of correspondence with server
                if not self.active: # shutting down
                    return
                # still active attempt to respawn server
                with self.__lock:
                    self.__spawn_server()
                continue
            print(f"RECEIVING DATA: {data}")
            self.receive(data)
        
