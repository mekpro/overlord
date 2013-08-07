import datetime
import logging
from pymongo import MongoClient

import config

def select_host(hostname):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  host = conn['host'].find_one({'hostname': hostname})
  return host

def select_group(groupname):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  group = conn['group'].find_one({'group': groupname})
  return group 

def initialize():
  pass

def hosts_same_group(host1, host2):
  if host1["group"] == host2["group"]:
    return True
  else:
    return False

def createIperfJob(src_host, dest_host):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  src_host['status'] = 'running'
  dest_host['status'] = 'running'
  conn['host'].update({"_id": src_host["_id"]}, src_host)
  conn['host'].update({"_id": dest_host["_id"]}, dest_host)
  return {'type':'iperf','hostname': dest_host["hostname"]}

def getJobForHost(src_hostname, dt):
  jobs = []
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  ping_dt = dt - config.PING_INTERVAL
  iperf_dt = dt - config.IPERF_INTERVAL
  iperf_hard_dt = dt - config.IPERF_HARD_INTERVAL
  src_host = select_host(src_hostname)

  # if my group is outside running
  #   query only inside group
  # else 
  #   run normally
    
  query = conn['flow'].find({
    'src' : src_hostname,
    'last_iperf_dt': {"$lt" : iperf_dt}
  })
  if config.ENABLE_HOSTGROUP:
    src_group = select_group(src_host["group"])
    if src_group["status"] == 'EXTERNAL':
      query[l'']
      # this won't work since flow doesn't know group_id
      # we may need to get members of group from query
      # and check it group memebership

  flows = query.sort('last_iperf_dt',1)
  # Do only one iperf to made the whole system work concurrently
  for flow in flows:
    dest_host = select_host(flow['dest'])
    # Soft Deadline
    if dest_host['status'] == 'idle':
      logging.error("soft:" + src_host["hostname"] + "->" + dest_host["hostname"])
      jobs.append(createIperfJob(src_host, dest_host))
      break;
    # Hard Deadline
    if dest_host['status'] == 'busy' and flow['last_iperf_dt'] < iperf_hard_dt:
      logging.error("hard:" + src_host["hostname"] + "->" + dest_host["hostname"])
      jobs.append(createIperfJob(src_host, dest_host))
      break;

  query = conn['flow'].find({
    'src' : src_hostname,
    'last_ping_dt': {"$lt" : ping_dt}
  })
  flows = query.sort('last_ping_dt',1)
  # Ping does not toggle host status to running, but need to be done when idle
  # Src host running is okay since it will complete iperf first btw
  for flow in flows:
    dest_host = select_host(flow['dest'])
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
  host_fe = select_host('fe')
  host_c0 = select_host('c0')
  host_c1 = select_host('c1')
  host_c2 = select_host('c2')
  host_c3 = select_host('c3')
  host_c4 = select_host('c4')
  host_c5 = select_host('c5')
  host_c6 = select_host('c6')
  print hosts_same_group(host_fe, host_c0)
  print hosts_same_group(host_c1, host_c0)
  print hosts_same_group(host_c2, host_c3)
  print hosts_same_group(host_c4, host_c6)
