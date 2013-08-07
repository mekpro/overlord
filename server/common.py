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

def select_host(hostname):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  host = conn['host'].find_one({'hostname': hostname})
  return host

def select_group(gid):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  group = conn['hostgroup'].find_one({'gid': gid})
  return group 

def hosts_same_group(host1, host2):
  if host1["gid"] == host2["gid"]:
    return True
  else:
    return False

def group_members(hostgroup):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  members = []
  query = conn['host'].find({'gid': hostgroup['gid']})
  for r in query:
    members.append(r['hostname'])
  return members

def update_group_status(src_group, src_host, dest_host):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  if not hosts_same_group(src_host, dest_host):
    src_group["status"] = 'external' 
  else:
    src_group["status"] = 'internal'
  conn['hostgroup'].update({"_id": src_group["_id"]}, src_group)
  

def createIperfJob(src_host, dest_host):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  src_host['status'] = 'running'
  dest_host['status'] = 'running'
  conn['host'].update({"_id": src_host["_id"]}, src_host)
  conn['host'].update({"_id": dest_host["_id"]}, dest_host)
  return {'type':'iperf','hostname': dest_host["hostname"]}

def initialize():
  pass

