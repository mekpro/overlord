import datetime
from pymongo import MongoClient
import logging

from server import config

HOSTS = ['fe','c0','c1','c2','c3','c4']
FLOWS = [
        ['c0','c1','c2','c3','c4'],
        ['fe','c2','c3'],
        ['fe','c4'],
        ['fe','c0','c1'],
        ['fe','c0','c2'],
        ['fe','c0','c1','c3']
        ]

def init_test_schema():
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  # Clear DB
  hostdb = conn['host']
  hostdb.drop()
  valuesdb = conn['values']
  valuesdb.drop()
  flowdb = conn['flow']
  flowdb.drop()

  # initdata 
  for hostname,flows in zip(HOSTS,FLOWS):
    h = {'hostname': hostname, 'authkey': 'none', 'status': 'idle'}
    hostdb.insert(h)
    for dest in flows:
      flow = {
        'src': hostname,
        'dest': dest,
        'last_iperf_dt': datetime.datetime(2000, 1, 1, 0, 0),
        'last_ping_dt': datetime.datetime(2000, 1, 1, 0, 0)
      }
      flowdb.insert(flow)

def get_flowlist(src_host):
  result = []
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  flows = conn.flow.find({'src' : src_host})
  for r in flows:
    result.append(r["dest"])
  return result

def create_values(value_type, values, start_dt, count, time_step):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  hosts_i = list(conn['host'].find())
  for i in hosts_i:
    hosts_j = get_flowlist(i["hostname"])
    for j in hosts_j:
      if i["hostname"] != j:
        for k in range(0,count):
          row = dict()
          row["type"] = value_type
          row["src"] = i["hostname"]
          row["dest"] = j
          for k1,v1 in values.items():
            row[k1] = v1
          row["dt"] = start_dt + datetime.timedelta(seconds=k*time_step)
          conn['values'].insert(row)

if __name__ == '__main__':
  ping_values = {'min': 0.42, 'max': 1.23, 'avg': 0.56, 'mdev': 0.04}
  iperf_values = {'bandwidth': 1234567}
  hosts = ['fe','c0','c1','c2', 'c3', 'c4', 'c5']
  count = 100
  time_step = 60
  start_dt = datetime.datetime.now() - datetime.timedelta(seconds=count*time_step)

  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  init_test_schema()
  print "hosts count: %d" %conn['host'].count()
  create_values('ping', ping_values, start_dt, count, time_step)
  print "values count: %d" %conn['values'].count()
  create_values('iperf', iperf_values, start_dt, count, time_step)
  print "values count: %d" %conn['values'].count()
