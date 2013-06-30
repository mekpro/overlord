from pymongo import MongoClient
import datetime
import logging
import config
import query
import random

def cleardb():
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  conn['host'].drop()
  conn['values'].drop()

def create_hosts(hosts):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  hostdb = conn['host']
  hostdb.drop()
  for hostname in hosts:
    h = {'hostname': hostname, 'authkey': 'none'}
    hostdb.insert(h)

def create_values(value_type, values, start_dt, count=1, time_step=60):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  hosts_i = list(conn['host'].find())
  hosts_j = list(conn['host'].find())
  for i in hosts_i:
    for j in hosts_j:
      if i["hostname"] != j["hostname"]:
        for k in range(0,count):
          row = dict()
          row["type"] = value_type
          row["src"] = i["hostname"]
          row["dest"] = j["hostname"]
          for k1,v1 in values.items():
            row[k1] = v1
          row["dt"] = start_dt + datetime.timedelta(seconds=k*time_step)
          conn['values'].insert(row)

if __name__ == '__main__':
  ping_values = {'min': 0.42, 'max': 1.23, 'avg': 0.56, 'mdev': 0.04}
  iperf_values = {'bandwidth': 1234567}
  hosts = ['fe','c0','c1','c2', 'c3', 'c4', 'c5']
  count = 10
  start_dt = datetime.datetime.now() - datetime.timedelta(count*time_step)

  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  cleardb()
  print "Database Cleared"

  create_hosts(hosts)
  print "hosts count: %d" %conn['host'].count()
  create_values('ping', ping_values, start_dt, count)
  print "values count: %d" %conn['values'].count()
  create_values('iperf', iperf_values, start_dt, count)
  print "values count: %d" %conn['values'].count()
 
  hostlist = query.hostlist()
  print hostlist
  print query.host_tables(hostlist[0], "ping")
  print query.graph()
  print query.host_query('fe','iperf','bandwidth','count',
