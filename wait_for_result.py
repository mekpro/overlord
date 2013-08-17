import time
import datetime
from pymongo import MongoClient

from server import config
from server import common

def get_unchecked_flow():
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  dt_after = datetime.datetime(2013, 1, 1, 0, 0)
  flow_query = {'last_iperf_dt': {'$lt' : dt_after}}
  flow = conn.flow.find(flow_query)
  return flow

def get_average_bandwidth(src_hostname):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  value_query = {'src' : src_hostname, 'type': 'iperf'}
  summation = 0
  count = 0
  for v in conn.values.find(value_query):
    summation += v["bandwidth"] 
    count += 1 
  return summation/count

if __name__ == '__main__':
  start_dt = datetime.datetime.now()
  while True:
    time.sleep(1)
    flows_unchecked = get_unchecked_flow()
    if flows_unchecked.count() == 0:
      print 'complete'
      time_to_complete = datetime.datetime.now() - start_dt
      print time_to_complete
      print get_average_bandwidth('fe') 
      print get_average_bandwidth('c0') 
      print get_average_bandwidth('c1') 
      break;
    else:
      pass
#      print 'waiting %d' %flows_unchecked.count()
#      if flows_unchecked.count() < 3:
#        for f in flows_unchecked:
#          print f

