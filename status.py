from pymongo import MongoClient
import sys
import common
import os
import time
from server import config
from server import common

def display():
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  grouplist = conn.hostgroup.find().sort('gid',1)
  print "Groups Status"
  for group in grouplist:
    print str(group["gid"]) + " : " + group["status"]
  
  print ""
  print "Hosts Status"
  hostlist = conn.host.find().sort('hostname',1)
  for host in hostlist:
    print host["hostname"] + " : " +host["status"]

if __name__ == '__main__':
  while True: 
    os.system('clear')
    display() 
    time.sleep(1)
