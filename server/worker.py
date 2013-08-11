import datetime
from pymongo import MongoClient
import logging
import time

import common
import config

def is_host_timeout(host, current_dt):
  if host['last_dt'] + config.STATE_TIMEOUT_INTERVAL > current_dt:
    return True
  else:
    return False

def record_state(host, current_dt):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  host_history = {
    'hostname' : host["hostname"],
    'status' : host["status"],
    'dt' : current_dt
  }
  conn['host_history'].insert(host_history)

# Worker run in daemon to check, made change and record to necesary time-based data
# Made change to status of non-reponsive agent host to 'timeout' state.
# Worker also keeps sampling of host status and record to 'host_history'

def main():
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  hostlist = list(conn["host"].find())
  while True:
    current_dt = datetime.datetime.now()
    for host in hostlist:
      if is_host_timeout(host, current_dt):
        host["status"] = 'timeout'
        conn.host.update({'_id': host["_id"]}, host)
      logging.error('recording %s,%s' %(host["hostname"], host["status"]))
      record_state(host, current_dt)
    time.sleep(config.STATE_SAMPLING_INTERVAL)
    logging.error('sleeping')

main()

