#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Abstract base classes for communicator"""

from abc import ABC, abstractmethod
import select

def poll(communicators, timeout=0):
    send_table = {}
    recv_table = {}

    write_fds = []
    read_fds = []
    # make a reverse dictionary of filenos to communicators
    for c in communicators:
        try:
            send_r, send_w, send_x = c.send_filenos()
            recv_r, recv_w, send_x = c.recv_filenos()
        except(OSError, EOFError):
            return True
        read_fds.extend(send_r + recv_r)
        write_fds.extend(send_w + recv_w)
        for fd in send_r + send_w:
            send_table[fd] = c
        for fd in recv_r + recv_w:
            recv_table[fd] = c
    # select file descriptors
    try:
        fds_r, fds_w, fds_x = select.select(read_fds, write_fds, [], timeout)
    except(OSError, EOFError):
        return True
    # extract communicators from communication table
    fds = fds_r + fds_w + fds_x
    recv_comms = set()
    send_comms = set()
    for fd in fds:
        try:
            recv_comms.add(recv_table[fd])
        except KeyError: # not in recv_table
            pass
        try:
            send_comms.add(send_table[fd])
        except KeyError:
            pass
    return (list(recv_comms), list(send_comms))

def poll_send(communicators, timeout=0):
    send_table = {}

    write_fds = []
    read_fds = []
    # make a reverse dictionary of filenos to communicators
    for c in communicators:
        try:
            send_r, send_w, send_x = c.send_filenos()
        except(OSError, EOFError):
            return True
        read_fds.extend(send_r)
        write_fds.extend(send_w)
        for fd in send_r + send_w:
            send_table[fd] = c
    # select file descriptors
    try:
        fds_r, fds_w, fds_x = select.select(read_fds, write_fds, [], timeout)
    except(OSError, EOFError):
        return True
    # extract communicators from communication table
    fds = fds_r + fds_w + fds_x
    return list({send_table[fd] for fd in fds})

def poll_recv(communicators, timeout=0):
    recv_table = {}

    write_fds = []
    read_fds = []
    # make a reverse dictionary of filenos to communicators
    for c in communicators:
        try:
            recv_r, recv_w, recv_x = c.recv_filenos()
        except(OSError, EOFError):
            return True
        read_fds.extend(recv_r)
        write_fds.extend(recv_w)
        for fd in recv_r + recv_w:
            recv_table[fd] = c
    # select file descriptors
    try:
        fds_r, fds_w, fds_x = select.select(read_fds, write_fds, [], timeout)
    except(OSError, EOFError):
        return True
    # extract communicators from communication table
    fds = fds_r + fds_w + fds_x
    return list({recv_table[fd] for fd in fds}) 
