from bottle import request, route, post, run
import bottle
import datetime
import pymongo
import logging

from schedulers import simple as scheduler

MEMCACHE_SERVER = 'localhost:11211'
IPERF_INTERVAL = 60
LISTEN_INTERVAL = 15

def authen(hostname, authkey):
  return True

def record_values(hostname, results):
  for r in results:
    logging.info("value : %s" %str(r))

def record_state(hostname, state):
  logging.info("host %s state %s" %(hostname,state))

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
  return result

if __name__ == '__main__':
  scheduler.initialize()
  run(host='localhost', port=8081)
