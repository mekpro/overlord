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
  return template('index_template', title="Overlord Monitoring" ,graph=graph, hostlist=hostlist, last_update=last_update)

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
  return template('host_template', title=hostname, hostname=hostname, hostlist=hostlist, last_update=last_update, ping_table=ping_table, iperf_table=iperf_table)

@route('/api')
def api_index():
  return template('api_index')

@route('/api/hostlist')
def api_hostlist():
  hostlist = query.hostlist()
  return {"result" : hostlist}

@route('/api/hoststats')
def api_hoststats():
  hoststats = query.hoststats()
  return {"result" : hoststats}

@route('/api/flowlist/<hostname>')
def api_flowlist(hostname):
  flowlist = query.flowlist(hostname)
  return {"result": flowlist}

@route('/api/flowstats/<hostname>')
def api_flowstats(hostname):
  flowstats = query.flowstats(hostname)
  return {"result": flowstats}

@route('/api/query/graph/<module>/<metric>')
def api_query_graph(module,metric):
  dt_start = datetime.datetime.now() - datetime.timedelta(minutes=5)
  dt_end = datetime.datetime.now()
  count = 5
  graph = query.graph_query(module, metric, count, dt_start, dt_end)
  return {"result": graph}

@route('/api/query/host/<hostname>/<module>/<metric>')
def api_query_host(hostname, module, metric):
  dt_start = datetime.datetime.now() - datetime.timedelta(minutes=10)
  dt_end = datetime.datetime.now()
  count = 5
  table = query.host_query(hostname, module, metric, count, dt_start, dt_end)
  return {"result": table}

if __name__ == '__main__':
  run (host='0.0.0.0', port=8082, debug=True,reloader=True)
