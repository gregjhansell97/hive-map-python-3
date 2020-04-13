#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pipe, Process
from multiprocessing.connection import Client, Listener, wait
from threading import Thread
import time

import hmap.communication.transceivers.abc as abc


def run_server(address):
    connections = [] # list of connections
    def manage_client(client):
        while True:
            try:
                raw_data = client.recv_bytes()
            except EOFError:
                # client is done
                connections.remove(client)
                client.close()
            for c in connections:
                if c is client:
                    # don't send a message back
                    continue
                # just try to send to other connections 
                c.send_bytes(raw_data)
    try:
        # gonna have problems with AF_UNIX on windows machines
        listener = Listener(address, family="AF_UNIX")
    except OSError:
        # possible loging
        print("failed to create daemon server")
        return # didn't work end process
    # go through and create connections
    while True:
        try:
            c = listener.accept()
        except Exception:
            print("ugh oh something went wrong")
            continue
        connections.append(c)
    listener.close()

def get_client_server(address):
    server = Process(target=run_server, args=(address,))
    server.start()
    client = None
    attempt = 0
    while client is None:
        try:
            client = Client(address, family="AF_UNIX")
        except FileNotFoundError:
            print("ipc file not responding")
        except ConnectionRefusedError:
            print("connection is refusing!")
        if attempt >= 3:
            attempt = 0
            print("Ineffective, restarting server process")
            # restart server_process
            if server.is_alive():
                server.kill()
            server.join()
            server = Process(target=run_server, args=(address,))
            server.start()
        attempt += 1
        time.sleep(0.5)
    if not server.is_alive():
        # server was not needed
        server.join()
        server = None 
    return (client, server)


def run_client(address, trx):
    client, server = get_client_server(address)
    connections = [client, trx]
    connections += [] if server is None else [server.sentinel]
    # go through and invoke on_recv when appropriate
    while True:
        responses = wait(connections)
        if server in responses: 
            # server is down! reset client and server
            print("server section")
            client.close()
            client, server = get_client_server(address)
            connections = [client, trx]
            connections += [] if server is None else [server.sentinel]
            continue
        if client in responses:
            print("client section")
            assert client.poll(0)
            try:
                data = client.recv_bytes()
            except EOFError:
                # server/client is down
                client.close()
                client, server = get_client_server()
                connections = [client, trx]
                connections += [] if server is None else [server.sentinel]
                continue
            trx.send_bytes(data)
        if trx in responses:
            print("trx section")
            assert trx.poll(0)
            try:
                data = trx.recv_bytes()
            except EOFError:
                # trx closed
                if server is not None:
                    server.kill()
                    server.join()
                client.close()
                trx.close()
                return 
            # successful
            client.send_bytes(data)

class Transceiver(abc.Transceiver):
    def __init__(self, address):
        super().__init__()
        # pass in a pipe that ends it
        client_pipe, trx_pipe = Pipe()
        self.__client_pipe = client_pipe
        self.__client = Process(target=run_client, args=(address, trx_pipe))
        self.__receive_loop = Thread(target=self.receive_loop)
        # go on ahead with or without connection
    def start(self): 
        self.__receive_loop.start()
        self.__client.start()
    def stop(self): 
        self.__client_pipe.close()
        self.__client.join()
        self.__receive_loop.join()
    def transmit(self, data):
        self.__client_pipe.send_bytes(data)
    def receive_loop(self):
        while True:
            try:
                data = self.__client_pipe.recv_bytes()
                self.receive(data)
            except EOFError:
                # end of correspondence with client
                break
        
