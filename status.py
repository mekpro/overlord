from pymongo import MongoClient
import sys
import common

from server import config

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
  display() 
