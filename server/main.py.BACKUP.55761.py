# from bottle import request, route, post, run
from bottle import request, post, run
# import bottle
import datetime
from pymongo import MongoClient
import logging

# import common
import config
import scheduler_timetable as scheduler


def authen(hostname, authkey):
    return True


def record_values(src_hostname, values):
<<<<<<< HEAD
    conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
    db_value = conn.values
    logging.error("values : %s" % str(values))
    for r in values:
        row = dict()
        row["src"] = src_hostname
        row["dt"] = datetime.datetime.now()
        row["dest"] = r["dest"]
        row["type"] = r["type"]
        if row["type"] == 'ping':
            row["min"] = int(r["min"])
            row["max"] = int(r["max"])
            row["avg"] = int(r["avg"])
            db_value.insert(row)
            logging.error("recording : %s" % str(row))
        elif row["type"] == 'iperf':
            row["bandwidth"] = int(r["bandwidth"])
            db_value.insert(row)
            logging.error("recording : %s" % str(row))
        else:
            logging.error("invalid value type: %s" % str(row["type"]))

=======
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  db_value = conn.values
  logging.error("values : %s" %str(values))
  for r in values:
    row = dict()
    row["src"] = src_hostname
    row["dt"] = datetime.datetime.now()
    row["dest"] = r["dest"]
    row["type"] = r["type"]
    if row["type"] == 'ping':
      row["min"] = r["min"] * 1000
      row["max"] = r["max"] * 1000
      row["avg"] = r["avg"] * 1000
      db_value.insert(row)
      logging.error("recording : %s" %str(row))
    elif row["type"] == 'iperf':
      row["bandwidth"] = int(r["bandwidth"])
      db_value.insert(row)
      logging.error("recording : %s" %str(row))
    else:
      logging.error("invalid value type: %s" %srow["type"])
>>>>>>> 32c5a0054e5168cfb73f384f51cd10cc3a7c1fa6

def record_state(hostname, state):
    logging.error("host %s state %s" % (hostname, state))


@post('/listen')
def index(hostname=0):
    d = request.json
    logging.info('POST request: %s' % str(d))
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
    conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
    hostdb = conn['host']
    hostdb.drop()
    valuesdb = conn['values']
    valuesdb.drop()
    hosts = ['fe', 'c0', 'c1', 'c2']
    for hostname in hosts:
        h = {'hostname': hostname, 'authkey': 'none'}
        hostdb.insert(h)

if __name__ == '__main__':
    init_test_data()
    scheduler.initialize()
    run(host='0.0.0.0', port=8081)
