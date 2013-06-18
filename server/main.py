from bottle import request, route, post, run
import bottle
import datetime
from pymongo import MongoClient
import logging

import common
import config
import scheduler_timetable as scheduler

def authen(hostname, authkey):
  return True

def record_values(src_hostname, values, dt):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  logging.error("values : %s" %str(values))
  for r in values:
    flow_query = {'src_host': src_hostname, 'dest_host': r["dest"]}
    flow = conn.flow.find_one(flow_query)
    row = dict()
    row["src"] = src_hostname
    row["dt"] = dt
    row["dest"] = r["dest"]
    row["type"] = r["type"]
    if row["type"] == 'ping':
      row["min"] = r["min"] * 1000
      row["max"] = r["max"] * 1000
      row["avg"] = r["avg"] * 1000
      flow["last_ping_dt"] = dt
    elif row["type"] == 'iperf':
      row["bandwidth"] = int(r["bandwidth"])
      flow["last_iperf_dt"] = dt
    else:
      logging.error("invalid value type: %s" %srow["type"])
      return False

    conn.values.insert(row)
    logging.error("recording : %s" %str(row))
    conn.flow.update(flow)
    logging.error("updating flow time: %s" %str(flow))

@post('/listen')
def index(hostname=0):
  d = request.json
  logging.info('POST request:' +str(d))
  if not authen(d["hostname"], d["authkey"]):
    return {'error': 'authenticate fail'}
  dt = datetime.datetime.now()
  record_values(d["hostname"], d["results"], dt)
  jobs = scheduler.getJobForHost(d["hostname"])
  result = dict()
  result['jobs'] = jobs
  logging.error(str(result))
  return result

if __name__ == '__main__':
  scheduler.initialize()
  run(host='0.0.0.0', port=8081)
