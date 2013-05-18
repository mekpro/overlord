import datetime
from pymongo import MongoClient
import pymongo
import logging
import random
import config

def load_hostlist():
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  hostlist = list()
  for host in conn.host.find():
    hostlist.append(host["hostname"])
  return hostlist

def initialize():
  hostlist = load_hostlist()

def getJobForHost(hostname):
  result = []
  hostlist = load_hostlist()
  nexthostid  = random.randint(0,len(hostlist)-1)
  result.append({'type': 'ping', 'hostname': hostlist[nexthostid]})
  result.append({'type': 'iperf', 'hostname': hostlist[nexthostid]})
  return result
