from bottle import request, route, post, run
import bottle
import datetime
from pymongo import MongoClient
import logging

import common
import scheduler_simple as scheduler

def authen(hostname, authkey):
  return True

def record_values(src_hostname, values):
  conn = MongoClient(common.MONGO_SERVER)[common.MONGO_DB]
  db_value = conn.values
  for r in values:
    row = dict()
    row["src"] = src_hostname
    row["dt"] = datetime.datetime.now()
    row["dest"] = r["dest"]
    row["type"] = r["type"]
    for k,v in r["values"].items():
      row[k] = v
    db_value.insert(row)
    logging.error("recording : %s" %str(row))

def record_state(hostname, state):
  logging.error("host %s state %s" %(hostname,state))

@post('/listen')
def index(hostname=0):
  d = request.json
  logging.info('POST request:' +str(d))
  if not authen(d["hostname"], d["authkey"]):
    return {'error': 'authenticate fail'}
  record_values(d["hostname"], d["results"])
  record_state(d["hostname"], d["state"])
  jobs = scheduler.getJobForHost(d["hostname"])
  result = dict()
  result['jobs'] = jobs
  logging.error(str(result))
  return result

def init_test_data():
  conn = MongoClient(common.MONGO_SERVER)[common.MONGO_DB]
  hostdb = conn['host']
  hostdb.drop()
  valuesdb = conn['values']
  valuesdb.drop()
  hosts = ['localhost']
#  hosts = ['fe','c0','c1','c2']
  for hostname in hosts:
    h = {'hostname': hostname, 'authkey': 'none'}
    hostdb.insert(h)

if __name__ == '__main__':
  init_test_data()
  scheduler.initialize()
  run(host='localhost', port=8081)
