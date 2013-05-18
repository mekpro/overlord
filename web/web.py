import bottle
from bottle import route, run, request, template
from bottle import static_file
from pymongo import MongoClient
import datetime
import json
import logging

import query
import config 

@route('/assets/<filepath:path>')
def server_static(filepath):
  return static_file(filepath, root=config.STATIC_ROOT)

@route('/')
def route_root():
  bottle.redirect("/index")

@route('/index')
def index():
  last_update = datetime.datetime.now()
  hostlist = query.hostlist()
  graph = json.dumps(query.graph())
  logging.error(graph)
  return template('index_template', graph=graph, hostlist=hostlist, last_update=last_update)

@route('/host')
def host():
  hostname = request.GET["hostname"]
  logging.error("hostname from GET: %s" %hostname)
  last_update = datetime.datetime.now()
  hostlist = query.hostlist()
  ping_table = query.host_tables(hostname, metric='ping')
  iperf_table = query.host_tables(hostname, metric='iperf')
  logging.error(ping_table)
  return template('host_template', hostname=hostname, hostlist=hostlist, last_update=last_update, ping_table=ping_table, iperf_table=iperf_table)

if __name__ == '__main__':
  run (host='0.0.0.0', port=8082, debug=True,reloader=True)
