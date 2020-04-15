#!/usr/bin/env python
# -*- coding: utf-8 -*-


def matching_interface():

    pass

def interest_serialize(interest):
    #TODO 
    pass

def event_serialization(event):
    # TODO
    pass

def interest_map(event, interest, disinterest):
    imap = interest.Map()
    imap.add(interest, 1) # adding value
    imap.add(disinterest, 2) # adding value

    # get all interests that would match event
    if set([1]) != set(imap.match(event)):
        return False
    
    # interest back isn't necessarily compatable but should end with same result
    interest.remove(disinterest, 2) # only interest remains now
    old_interests = imap.interests
    imap= interest.Map() # new imap
    for i in old_interests:
        imap.add(i, 1)
    imap.add(disinterest, 2)
    # get all interests that would match event
    if set([1]) != set(imap.match(event)):
        return False
    # test success!
    return True
    
