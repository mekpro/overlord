import datetime
import logging
from pymongo import MongoClient

import config
import common

def initialize():
  pass

def getJobForHost(src_hostname, dt):
  jobs = []
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  ping_dt = dt - config.PING_INTERVAL
  iperf_dt = dt - config.IPERF_INTERVAL
  iperf_hard_dt = dt - config.IPERF_HARD_INTERVAL
  src_host = common.select_host(src_hostname)


  query = {
    'src' : src_hostname,
    'last_iperf_dt': {"$lt" : iperf_dt}
  }
  src_group = common.select_group(src_host["gid"])
  if config.ENABLE_HOSTGROUP:
    if src_group["status"] == 'external':
      members = common.group_members(src_group)
      logging.error("internal members :%s" %str(members))
      query['dest'] = { "$in": members}

  running_hosts = conn.host.find({'status':'running'}).count()
  if running_hosts >= config.MAX_RUNNING:
    query['src'] = 'this should found nothing'

  flows = conn.flow.find(query).sort('last_iperf_dt',1)
  logging.error("flows count: %d " %flows.count())
  # Do only one iperf to made the whole system work concurrently
  for flow in flows:
    dest_host = common.select_host(flow['dest'])
    dest_group = common.select_group(dest_host["gid"])
    # Soft Deadline
    if dest_host['status'] == 'idle':
      logging.error("soft:" + src_host["hostname"] + "->" + dest_host["hostname"])
      jobs.append(common.createIperfJob(src_host, dest_host))
      common.update_group_status(src_group, dest_group)
      break;
    # Hard Deadline
    if dest_host['status'] == 'busy' and flow['last_iperf_dt'] < iperf_hard_dt:
      logging.error("hard:" + src_host["hostname"] + "->" + dest_host["hostname"])
      jobs.append(common.createIperfJob(src_host, dest_host))
      common.update_group_status(src_group, dest_group)
      break;

  query = conn['flow'].find({
    'src' : src_hostname,
    'last_ping_dt': {"$lt" : ping_dt}
  })
  flows = query.sort('last_ping_dt',1)
  # Ping does not toggle host status to running, but need to be done when idle
  # Src host running is okay since it will complete iperf first btw
  for flow in flows:
    dest_host = common.select_host(flow['dest'])
    if dest_host['status'] == 'idle':
      jobs.append({'type':'ping','hostname': dest_host["hostname"]})

  return jobs

if __name__ == '__main__':
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
#  iperf_dt = datetime.datetime.now() - IPERF_INTERVAL
  dt = datetime.datetime(2013, 1,1, 0,0,0)
  jobs = getJobForHost('fe', dt)
  print jobs
  # tester: running=2 
  running_count = conn['host'].find({'status': 'running'}).count()
  if running_count != 2:
    print "error running != 2 , =%d" %running_count
  host_fe = common.select_host('fe')
  host_c0 = common.select_host('c0')
  host_c1 = common.select_host('c1')
  host_c2 = common.select_host('c2')
  host_c3 = common.select_host('c3')
  host_c4 = common.select_host('c4')
  host_c5 = common.select_host('c5')
  host_c6 = common.select_host('c6')
  print common.hosts_same_group(host_fe, host_c0)
  print common.hosts_same_group(host_c1, host_c0)
  print common.hosts_same_group(host_c2, host_c3)
  print common.hosts_same_group(host_c4, host_c6)
