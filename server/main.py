from bottle import request, route, post, run
import bottle
import datetime
from pymongo import MongoClient
import logging

import common
import config
import scheduler_idlewait as scheduler

def authen(hostname, authkey):
  return True

def record_values(src_hostname, status, values, dt):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  logging.error(src_hostname +" - values : " +str(values))
  src_host = common.select_host(src_hostname)
  src_group = common.select_group(src_host["gid"])
  for r in values:
    row = dict()
    row["src"] = src_hostname
    row["dt"] = dt
    row["type"] = r["type"]
    row["dest"] = r["dest"]
    if row["type"] == 'utilization':
      row["cpu"] = float(r["cpu"])
      row["net"] = float(r["net"])
      row["loadavg"] = float(r["loadavg"])
    else:
      flow_query = {'src': src_hostname, 'dest': r["dest"]}
      flow = conn.flow.find_one(flow_query)
      if row["type"] == 'ping':
        row["min"] = float(r["min"])
        row["max"] = float(r["max"])
        row["avg"] = float(r["avg"])
        flow["last_ping_dt"] = dt
      elif row["type"] == 'iperf':
        row["bandwidth"] = float(r["bandwidth"])
        flow["last_iperf_dt"] = dt
      else:
        logging.error("invalid value type")
        return False
      conn.flow.update({'_id': flow["_id"]}, flow)

    conn.values.insert(row)
    logging.error("recording : %s" %str(row['src']))

  if status == 'idle':
    src_host["status"] = 'idle'
    src_group["status"] = 'idle'
    conn.hostgroup.update({'_id':src_group["_id"]}, src_group)
  else: 
    src_host["status"] = status
  conn.host.update({'_id':src_host["_id"]}, src_host)

@post('/listen')
def listen():
  d = request.json
#  logging.error('POST request:' +str(d))
  if not authen(d["hostname"], d["authkey"]):
    return {'error': 'authenticate fail'}
  dt = datetime.datetime.now()
  record_values(d["hostname"], d["status"], d["results"], dt)
  return {'status': 'ok'}

@post('/getjobs')
def getjobs():
  d = request.json
  if not authen(d["hostname"], d["authkey"]):
    return {'error': 'authenticate fail'}
  dt = datetime.datetime.now()
  jobs = scheduler.getJobForHost(d["hostname"], dt)
  result = {'jobs': jobs}
  return result

if __name__ == '__main__':
  scheduler.initialize()
  run(server='paste', host='0.0.0.0', port=8081)
