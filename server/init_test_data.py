import datetime
from pymongo import MongoClient
import logging

import common
import config

HOSTS = ['fe','c0','c1','c2','c3','c4']
FLOWS = [
        ['c0','c1','c2','c3','c4'],
        ['fe','c2','c3'],
        ['fe','c4'],
        ['fe','c0','c1'],
        ['fe','c0','c2'],
        ['fe','c0','c1','c3']
        ]

def init_test_data():
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
      flow = {'src': hostname, 'dest': dest,
        'last_iperf_dt': datetime.datetime(2000, 1, 1, 0, 0),
        'last_ping_dt': datetime.datetime(2000, 1, 1, 0, 0)
      }
      flowdb.insert(flow)

def create_sample_data():
 pass

if __name__ == '__main__':
  init_test_data()
