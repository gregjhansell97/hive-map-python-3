# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound

from hmap.interface.utils import has_traits
from hmap.interface.communication import Communicator
from hmap.interface.matching import Event, Subscription, Interest
from hmap.interface.routing import Router

__all__ = ["has_traits", "Communicator", "Event", "Subscription", 
        "Interest", "Router"]
