# import datetime
# from pymongo import MongoClient
# import pymongo
# import logging
import random

# import common
from common import load_hostlist
# import config


def initialize():
    """
    Do neccessary data initialize for this scheduler
    """
    pass


def getJobForHost(hostname):
    """
    Return job list of job ([{'type','hostname'}]) for the requested host.
    Return blank list if no job is currently needed.
    """
    result = []
    hostlist = load_hostlist()
    nexthostid    = random.randint(0, len(hostlist)-1)
    result.append({'type': 'ping', 'hostname': hostlist[nexthostid]})
    result.append({'type': 'iperf', 'hostname': hostlist[nexthostid]})
    return result
