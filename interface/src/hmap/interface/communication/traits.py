#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class Pollable(ABC):
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


__all__ = ["Pollable"]
