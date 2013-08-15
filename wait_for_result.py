import time
import datetime
from pymongo import MongoClient

from server import config
from server import common

def get_unchecked_flow():
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  dt_after = datetime.datetime(2013, 1, 1, 0, 0)
  flow_query = {'last_iperf_dt': {'$lt' : dt_after}}
  flow_count = conn.flow.find(flow_query).count()
  return flow_count

if __name__ == '__main__':
  while True:
    time.sleep(1)
    flows_unchecked = get_unchecked_flow()
    if flows_unchecked == 0:
      print 'complete'
    else:
      print 'waiting %d' %flows_unchecked

