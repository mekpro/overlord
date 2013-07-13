import datetime
import logging
from pymongo import MongoClient

import config

def select_host(hostname):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  host = conn['host'].find_one({'hostname': hostname})
  return host

def initialize():
  pass

def getJobForHost(src_hostname, dt):
  jobs = []
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  ping_dt = dt - config.PING_INTERVAL
  iperf_dt = dt - config.IPERF_INTERVAL
  src_host = select_host(src_hostname)

  query = conn['flow'].find({
    'src' : src_hostname,
    'last_iperf_dt': {"$lt" : iperf_dt}
  })
  flows = query.sort('last_iperf_dt',1)
  # Do only one iperf to made the whole system work concurrent
  for flow in flows:
    dest_host = select_host(flow['dest'])
    logging.error(dest_host)
    if dest_host['status'] == 'idle':
      jobs.append({'type':'iperf','hostname': dest_host["hostname"]})
      src_host['status'] = 'busy'
      conn['host'].update({"_id": src_host["_id"]}, src_host)
      dest_host['status'] = 'busy'
      conn['host'].update({"_id": dest_host["_id"]}, dest_host)
      break;

  query = conn['flow'].find({
    'src' : src_hostname,
    'last_ping_dt': {"$lt" : ping_dt}
  })
  flows = query.sort('last_ping_dt',1)
  # Ping does not toggle host status to busy, but need to be done when idle
  # Src host busy is okay since it will complete iperf first btw
  for flow in flows:
    dest_host = select_host(flow['dest'])
    logging.error(dest_host)
    if dest_host['status'] == 'idle':
      jobs.append({'type':'ping','hostname': dest_host["hostname"]})

  return jobs

if __name__ == '__main__':
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
#  iperf_dt = datetime.datetime.now() - IPERF_INTERVAL
  dt = datetime.datetime(2013, 1,1, 0,0,0)
  jobs = getJobForHost('fe', dt)
  print jobs
  # tester: busy=2 
  busy_count = conn['host'].find({'status': 'busy'}).count()
  if busy_count != 2:
    print "error busy != 2 , =%d" %busy_count
