#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
from multiprocessing import Pipe, Process
from multiprocessing.connection import Client, Listener, wait
import select
from threading import Thread, Lock
import time

from hmap.interface.communication import Communicator


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
                with session.lock:
                    for c in connections:
                        if c is client:
                            continue
                        c.send_bytes(data)
                # TODO PLOP IN WHAT's below
            except(EOFError, ConnectionResetError, ConnectionRefusedError, 
                    FileNotFoundError, BrokenPipeError, OSError):
                # something went wrong with client, connection is broken beyond
                # recovery
                with session.lock:
                    connections.remove(client)
                    client.close()
                    if len(connections) == 0:
                        # no more connections, poison process
                        session.stop = True
                        try:
                            poison_client = Client(address, family="AF_UNIX")
                        except(ConnectionRefusedError, FileNotFoundError): 
                            # process dieing or already dead
                            pass
                return # exit the thread
    try:
        # gonna have problems with AF_UNIX on windows machines
        listener = Listener(address, family="AF_UNIX")
    except:
        trx.send_bytes(b"0") # didn't work
        return
    with listener:
        trx.send_bytes(b"1") # successfully created listener
        #NOTE do not use trx after this point
        # go through and create connections
        while True:
            # gotta accept at least one client
            c = listener.accept()
            if session.stop:
                # client warned me to stop
                return 
            with session.lock:
                connections.append(c)
            threads.append(
                    Thread(target=manage_client, args=[c], daemon=True))
            threads[-1].start()

class IPCTransceiver(Communicator):
    def __repr__(self):
        return f"IPCTransceiver({self.__address})"
    def __init__(self, name=None, address=None):
        super().__init__()
        # pass in a pipe that ends it
        if address is None and name is None:
            raise ValueError("address and name kwargs cannot both be None")
        if address is None:
            address = f"./.{name}.ipc"
        self.__address = address
        self.__close_trigger, self.__close_flag = Pipe()
        self.__server_lock = Lock()
        self.__server = self.__get_server()
        # registers ctrl-c and exit
        #atexit.register(self.close) # TODO add to super class 
    def __get_server(self):
        address = self.__address
        # start-up the session
        server, client = Pipe()
        daemon = Process(
                target=session, args=((address, client)))
        daemon.start()
        # wait for either server to fail or succeed
        success = (server.recv_bytes() == b"1")
        # if it failed some other process has created the server or! 
        # there is some ipc file that is impedeing it...
        # close pipes regardless
        client.close()
        server.close()
        # create client called server b/c server is being accessed
        return Client(address, family="AF_UNIX")
    def close(self): 
        if self.__close_flag.poll():
            return
        self.__close_trigger.send(b"1")
        with self.__server_lock:
            self.__server.close()
    def send(self, data, timeout=None):
        try:
            self.__server.send_bytes(data)
        except(OSError, AttributeError, BrokenPipeError): # file is closed
            raise EOFError
    def recv(self, timeout=None):
        if self.__close_flag.poll():
            raise EOFError
        while True:
            with self.__server_lock:
                responses = wait(
                        [self.__server, self.__close_flag],
                        timeout=timeout)
                if self.__close_flag in responses:
                    raise EOFError # end of session, self.close invoked
                if len(responses) == 0: 
                    # timeout occurred
                    return b""
                try:
                    data = self.__server.recv_bytes()
                except EOFError:
                    # file was closed attempt to recover the server
                        if self.__close_flag.poll():
                            # self is closing, no use recovering server
                            raise EOFError
                        self.__server = self.__get_server()
                else:
                    return data
    def send_filenos(self):
        return ([self.__close_flag], [self.__server.fileno()], [])
    def recv_filenos(self):
        return ([self.__close_flag, self.__server.fileno()], [], [])

