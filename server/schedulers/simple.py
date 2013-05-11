import datetime
import pymongo
import logging
import random

MEMCACHE_SERVER = 'localhost:11211'
IPERF_INTERVAL = 60
LISTEN_INTERVAL = 15

def load_hostlist():
  hostlist = [
    'localhost',
  ]
  return hostlist

def initialize():
  hostlist = load_hostlist()

def getJobForHost(hostname):
  result = []
  hostlist = load_hostlist()
  nexthostid  = random.randint(0,len(hostlist)-1)
  result.append(hostlist[nexthostid])
  return result
