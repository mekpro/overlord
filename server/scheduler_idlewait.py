import datetime
import logging
from pymongo import MongoClient

import init_test_data
import config

IPERF_INTERVAL = datetime.timedelta(minutes=0)
PING_INTERVAL = datetime.timedelta(minutes=1)

def select_host(hostname):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  host = conn['host'].find_one({'hostname': hostname})
  return host

def initialize():
  pass

def getJobForHost(src_hostname, iperf_dt):
  jobs = []
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  src_host = select_host(src_hostname)
  query = conn['flow'].find({
    'src' : src_hostname,
    'last_iperf_dt': {"$lt" : iperf_dt}
  })
  flows = query.sort('last_iperf_dt',1)
  logging.error("flows count: %d" %flows.count())
  for flow in flows:
    dest_host = select_host(flow['dest'])
    logging.error(dest_host)
    if dest_host['status'] == 'idle':
      jobs.append({'type':'iperf','hostname': dest_host["hostname"]})
      src_host['status'] = 'busy'
      conn['host'].update({"_id": src_host["_id"]}, src_host)
      dest_host['status'] = 'busy'
      conn['host'].update({"_id": dest_host["_id"]}, dest_host)
    else:
      logging.error('destination busy %s' %str(dest_host))

  return jobs

if __name__ == '__main__':
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  init_test_data.init_test_data()
#  iperf_dt = datetime.datetime.now() - IPERF_INTERVAL
  iperf_dt = datetime.datetime(2010, 1,1, 0,0,0)
  jobs = getJobForHost('fe', iperf_dt)
  print jobs
  # tester: next job should equal to busy and self 
  busy_count = conn['host'].find({'status': 'busy'}).count()
  if busy_count != len(jobs) + 1:
    print "error busy = %d , jobs = %d" %(busy_count, len(jobs))
  # tester: next job should equal number of flow and self
  flow_count = conn['flow'].find({'src': 'fe'}).count()
  if flow_count != len(jobs) + 1:
    print "error flow_count = %d , jobs = %d" %(flow_count, len(jobs))
