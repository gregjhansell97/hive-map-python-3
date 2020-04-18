#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Abstract base classes for communicator"""

from abc import ABC, abstractmethod
import atexit
import math
import select
import weakref


class Communicator(ABC):
    """Abstract base class for all communicators. Communicators send to one
    or more other communicators and receive data from one or more communicators.
    """
    __instances = []
    def __init__(self):
        Communicator.__instances.append(weakref.ref(self))
    def __del__(self): 
        self.close()

    @abstractmethod
    def send(self, data, timeout=None):
        """Sends data to one or more communicators
        
        Args:
            data(bytes): data to send to other communicators

        Raises:
            - if data is too large
            - if data are not bytes
            - if transceiver is closed while transmiting
            - if past timeout and couldn't send information
        """
        raise NotImplementedError
    def poll_send(self, data, timeout=None):
        """Returns True if communicator can send information at that time or the
        communicator has been closed"""
        return select.select(*self.send_filenos(), timeout) != ([], [], [])

    @abstractmethod
    def recv(self, timeout=None):
        """Receives data from another communicator, blocks for duration of
        timeout. If timeout is set to None, then blocks indefinitely

        Args:
            timeout: duration of blocking call

        Returns:
            (bytes): data received

        Raises:
            - if there is too much data received
            - if transceiver is closed while receiving
            - if passed timeout and didn't receive any bytes
        """
        raise NotImplementedError
    def poll_recv(self, timeout=None):
        """Returns True if communicator can receive information at that time or
        the communicator has been closed"""
        return select.select(*self.recv_filenos, timeout) != ([], [], [])

    @abstractmethod
    def close(self):
        """
        Idempotent function that ends send and recv capabilities
        """
        raise NotImplementedError

    @abstractmethod
    def send_filenos(self):
        """Returns a 3-D tuple of lists. These file descriptors indicate when
        the communicator is ready to send information or has been closed.
        The first list is a list of file discriptors to check for read status, 
        and the second list is a list of file descriptors to check for 
        write status, the third checks for 'exceptional conditions'
        """
        raise NotImplementedError

    @abstractmethod
    def recv_filenos(self):
        """Returns a 2-D tuple of lists. These file descriptors indicate when
        the communicator is ready to receive information or has been closed.
        The first list is a list of file discriptors to check for read status, 
        and the second list is a list of file descriptors to check for 
        write status, the third checks for 'exceptional conditions'
        """
        raise NotImplementedError

    @atexit.register
    def __clean_up():
        comms = [t() for t in Communicator.__instances if t() is not None]
        for c in comms:
            c.close()

def poll(communicators, timeout=None):
    send_table = {}
    recv_table = {}

    write_fds = []
    read_fds = []
    # make a reverse dictionary of filenos to communicators
    for c in communicators:
        send_r, send_w = c.send_filenos()
        recv_r, recv_w = c.recv_filenos()
        read_fds.extend(send_r + recv_r)
        write_fds.extend(send_w + recv_w)
        for fd in send_r + send_w:
            send_table[fd] = c
        for fd in recv_r + recv_w:
            recv_table[fd] = c
    # select file descriptors
    fds_r, fds_w, fds_x = select.select(read_fds, write_fds, [], timeout)
    # extract communicators from communication table
    fds = fds_r + fds_w + fds_x
    return (
            list({recv_table[fd] for fd in fds}), 
            list({send_table[fd] for fd in fds}))

def poll_send(communicators, timeout=None):
    send_table = {}

    write_fds = []
    read_fds = []
    # make a reverse dictionary of filenos to communicators
    for c in communicators:
        send_r, send_w = c.send_filenos()
        read_fds.extend(send_r)
        write_fds.extend(send_w)
        for fd in send_r + send_w:
            send_table[fd] = c
    # select file descriptors
    fds_r, fds_w, fds_x = select.select(read_fds, write_fds, [], timeout)
    # extract communicators from communication table
    fds = fds_r + fds_w + fds_x
    return list({send_table[fd] for fd in fds})

def poll_recv(communicators, timeout=None):
    recv_table = {}

    write_fds = []
    read_fds = []
    # make a reverse dictionary of filenos to communicators
    for c in communicators:
        recv_r, recv_w = c.recv_filenos()
        read_fds.extend(recv_r)
        write_fds.extend(recv_w)
        for fd in recv_r + recv_w:
            recv_table[fd] = c
    # select file descriptors
    fds_r, fds_w, fds_x = select.select(read_fds, write_fds, [], timeout)
    # extract communicators from communication table
    fds = fds_r + fds_w + fds_x
    return list({recv_table[fd] for fd in fds}) 



# TODO write a base class for packing a message
