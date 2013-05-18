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


