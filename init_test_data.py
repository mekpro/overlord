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
        ['c1', 3],
        ['c2', 4],
        ['c3', 2],
        ['c4', 3],
        ['c5', 4],
        ['c6', 2],
        ['c7', 3],
        ['c8', 4],
        ['c9', 2],
        ['c10', 3],
        ['c11', 4],
        ['c12', 2],
        ['c13', 3],
        ['c14', 4],
        ]
FLOWS = [
        ['c1','c2','c3','c4','c5','c6'],
        ['c3','c6','c9','c12'],
        ['fe','c4','c8','c14'],
        ['c5','c3','c11','c13'],
        ['c8','c9','c2','c7','c10'],
        ['fe','c9','c12','c14'],
        ['c2','c4','c11','c13'],
        ['fe','c2','c7','c6'],
        ['fe','c1','c3','c8','c12'],
        ['c13','c0','c4','c9'],
        ['fe','c5','c14','c13'],
        ['c1','c3','c5','c10','c12'],
        ['c8','c3','c5','c6','c9'],
        ['c5','c6','c10','c14'],
        ['c5','c7','c8','c11'],
        ['c2','c11','c12','c14'],
        ['c2','c3','c9','c10'],
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
  hostgroupdb = conn['hostgroup']
  hostgroupdb.drop()

  # initdata 
  for group in range(1,GROUP_COUNT+1):
    g = {
      'gid': group,
      'status': 'idle', # idle, internal, external 
    }
    hostgroupdb.insert(g)

  for hostname,flows in zip(HOSTS,FLOWS):
    h = {
      'hostname': hostname[0],
      'authkey': 'none',
      'status': 'idle', # idle, busy, down
      'last_dt': datetime.datetime(2000, 1, 1, 0, 0),
      'gid': hostname[1],
      'uname_r': '3.11.0-12-generic',
      'uname_i': 'x86_64',
      'cpu_name': 'Intel(R) Core(TM) i5-3210M CPU @ 2.50GHz',
      'cpu_cores': 2,
      'latitude': random.randint(1,10000000) / 1000000.0,
      'longtitude': random.randint(1,10000000) / 1000000.0
    }
    hostdb.insert(h)
    for dest in flows:
      flow = {
        'src': hostname[0],
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

