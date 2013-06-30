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
def index_view():
  last_update = datetime.datetime.now()
  hostlist = query.hostlist()
  graph = json.dumps(query.graph_force())
  logging.error(graph)
  return template('index_template', graph=graph, hostlist=hostlist, last_update=last_update)

@route('/chordgraph')
def chordgraph_view():
  return template('chordgraph_template')

@route('/calendar')
def calendar_view():
  return template('calendar_template')

@route('/heatmap/daily')
def heatmap_daily_view():
  return template('heatmap_template')

@route('/host')
def host_view():
  hostname = request.GET["hostname"]
  logging.error("hostname from GET: %s" %hostname)
  last_update = datetime.datetime.now()
  hostlist = query.hostlist()
  ping_table = query.host_tables(hostname, metric='ping')
  iperf_table = query.host_tables(hostname, metric='iperf')
  logging.error(ping_table)
  return template('host_template', hostname=hostname, hostlist=hostlist, last_update=last_update, ping_table=ping_table, iperf_table=iperf_table)

@route('/api')
def api_view():
  action = request.GET["action"]
  if action == 'hostList':
    result = query.hostlist()
  elif action == 'hostsInfo':
    result = [
      {'hostname': 'host1' , 'status': 'idle', 'last_update': datetime.datetime.now()},
      {'hostname': 'host2' , 'status': 'busy', 'last_update': datetime.datetime.now()},
      {'hostname': 'host3' , 'status': 'down', 'last_update': datetime.datetime.now()}
    ]

  elif action == 'queryGraph':
    pass

  elif action == 'queryValues':
    pass

  else:
    logging.error('Invalid api action: %s' %action)
    result = ''
  return json.dumps(result)

if __name__ == '__main__':
  run (host='1.0.0.0', port=8082, debug=True,reloader=True)
