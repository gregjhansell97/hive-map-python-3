#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.communication.fixtures import FCommunication

def test_communicator_uniqueness(FCommunication):
    instances = FCommunication.instances(10)
    assert len(instances) == len(set(instances))
