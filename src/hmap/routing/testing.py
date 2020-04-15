#!/usr/bin/env python
# -*- coding: utf-8 -*-

def start_stop(router):
    router.start()
    # check for idempodency of start
    for i in range(10):
        router.start()
    router.stop()
    # check for idempodency of stop
    for i in range(10):
        router.stop()
    return True

def enter_exit(router):
    for i in range(10):
        with router:
            pass
    # let's raise an exception!
    try:
        with router:
            raise ValueError
    except ValueError:
        pass
    except:
        return False # don't change the error
    else:
        return False # don't surpress the error
    # should return and exit router
    with router:
        return True

def router_test(test):
    def wrapper(router, *args, **kwargs):
        with router:
            return test(router, *args, **kwargs)

@router_test
def topic_based_interaction_flat_int_pyobj(router):
    router.subscribe(1, callback)
    
