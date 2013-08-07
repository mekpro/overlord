import datetime
from pymongo import MongoClient
import logging
import random
import sys

from server import config

GROUP_COUNT = 4

HOSTS = [
        ['fe', 1],
        ['c0', 2],
        ['c1', 2],
        ['c2', 3],
        ['c3', 3],
        ['c4', 4],
        ['c5', 4],
        ['c6', 4],
        ]
FLOWS = [
        ['c0','c1','c2','c3','c4','c5','c6'],
        ['fe','c2','c3','c6'],
        ['fe','c4'],
        ['fe','c0','c1','c4'],
        ['fe','c0','c2'],
        ['fe','c0','c1','c3'],
        ['fe','c2','c3','c4'],
        ['fe','c1','c6'],
        ['fe','c1','c3','c5'],
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
  groupdb = conn['group']
  groupdb.drop()

  # initdata 
  for group in range(1,GROUP_COUNT):
    g = {
      'group': group,
      'status': 'IDLE', # IDLE, INTERNAL, EXTERNAL
    }
    groupdb.insert(g)

  for hostname,flows in zip(HOSTS,FLOWS):
    h = {
      'hostname': hostname[0],
      'authkey': 'none',
      'status': 'idle',
      'last_dt': datetime.datetime(2000, 1, 1, 0, 0),
      'group': hostname[1] 
    }
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
          if value_type == 'iperf':
            row["bandwidth"] = random.randint(0,100)
          row["dt"] = start_dt + datetime.timedelta(seconds=k*time_step)
          conn['values'].insert(row)

def create_host_history(start_dt, count, time_step):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  hosts = list(conn['host'].find())
  state_list = ['idle','idle','idle','timeout','busy','running','running']
  for host in hosts:
    for k in range(0,count):
      row = dict()
      row["hostname"] = host["hostname"]
      row["dt"] = start_dt + datetime.timedelta(seconds=k*time_step)
      status = state_list[random.randint(0,len(state_list)-1)]
      row["status"] = status
      conn['host_history'].insert(row)

if __name__ == '__main__':
  count = 0
  if len(sys.argv) == 2:
    count = int(sys.argv[1])
  else:
    print 'python init_test_data.py [size]'
    print 'put size = 0 to only initiate schema'
    sys.exit(0)

  ping_values = {'min': 0.42, 'max': 1.23, 'avg': 0.56, 'mdev': 0.04}
  iperf_values = {'bandwidth': 1234567}
  hosts = ['fe','c0','c1','c2', 'c3', 'c4', 'c5']
  time_step = 300
  start_dt = datetime.datetime.now() - datetime.timedelta(seconds=count*time_step)

  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  init_test_schema()
  print "hosts count: %d" %conn['host'].count()
  create_values('ping', ping_values, start_dt, count, time_step)
  print "values count: %d" %conn['values'].count()
  create_values('iperf', iperf_values, start_dt, count, time_step)
  print "values count: %d" %conn['values'].count()
  create_host_history(start_dt, count, time_step)

