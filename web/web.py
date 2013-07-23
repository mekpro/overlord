import bottle
from bottle import get, post, route, run, request, template
from bottle import static_file
from pymongo import MongoClient
import datetime
import json
import logging

import query
import config

def api_dt_start(request):
  if 'dt_start' not in request.GET:
    dt_start = datetime.datetime.now() - datetime.timedelta(minutes=120)
  else:
    dt_start = query.dt_from_timestamp(float(request.GET['dt_start']))
  return dt_start

def api_dt_end(request):
  if 'dt_end' not in request.GET:
    dt_end = dt_start + datetime.timedelta(minutes=120)
  else:
    dt_end = query.dt_from_timestamp(float(request.GET['dt_end']))
  return dt_end

def web_dt_start(request):
  if request.forms.get('dt_start') == '':
    dt_start = datetime.datetime.now() - datetime.timedelta(hours=2)
  else:
    dt_start = query.parse_form_dt(request.forms.get('dt_start'))
  return dt_start

def web_dt_end(request):
  if request.forms.get('dt_end') == '':
    dt_end = dt_start + datetime.timedelta(hours=2)
  else:
    dt_end = query.parse_form_dt(request.forms.get('dt_end'))
  return dt_end

@get('/assets/<filepath:path>')
def server_static(filepath):
  return static_file(filepath, root=config.STATIC_ROOT)

@get('/')
def route_root():
  bottle.redirect("/index")

@get('/index')
def index_view():
  last_update = datetime.datetime.now()
  hostlist = query.hostlist()
  graph = json.dumps(query.graph_force())
  logging.error(graph)
  return template('index_template', title="Overlord Monitoring" ,graph=graph, hostlist=hostlist, last_update=last_update)

@get('/chordgraph')
def chordgraph_view():
  return template('chordgraph_template')

@get('/calendar')
def calendar_view():
  return template('calendar_template')

@get('/heatmap/daily')
def heatmap_daily_view():
  return template('heatmap_template')

@get('/host/<hostname>')
def host_view(hostname):
  last_update = datetime.datetime.now()
  dt_start = datetime.datetime.now() - datetime.timedelta(hours=2)
  dt_end = datetime.datetime.now()
  hostlist = query.hostlist()
  ping_table = query.host_tables(hostname, metric='ping')
  iperf_table = query.host_tables(hostname, metric='iperf')
  return template('host_template', title=hostname, hostname=hostname, hostlist=hostlist, last_update=last_update, dt_start=query.dt_to_timestamp(dt_start), dt_end=query.dt_to_timestamp(dt_end), ping_table=ping_table, iperf_table=iperf_table)

@post('/host/<hostname>')
def host_view_post(hostname):
  dt_start = web_dt_start(request)
  dt_end = web_dt_end(request)
  last_update = datetime.datetime.now()
  hostlist = query.hostlist()
  ping_table = query.host_tables(hostname, metric='ping')
  iperf_table = query.host_tables(hostname, metric='iperf')
  return template('host_template', title=hostname, hostname=hostname, hostlist=hostlist, last_update=last_update, dt_start=query.dt_to_timestamp(dt_start), dt_end=query.dt_to_timestamp(dt_end), ping_table=ping_table, iperf_table=iperf_table)


@get('/api')
def api_index():
  return template('api_index')

@get('/api/hostlist')
def api_hostlist():
  hostlist = query.hostlist()
  return {"result" : hostlist}

@get('/api/hoststats')
def api_hoststats():
  hoststats = query.hoststats()
  return {"result" : hoststats}

@get('/api/flowlist/<hostname>')
def api_flowlist(hostname):
  flowlist = query.flowlist(hostname)
  return {"result": flowlist}

@get('/api/flowstats/<hostname>')
def api_flowstats(hostname):
  flowstats = query.flowstats(hostname)
  return {"result": flowstats}

@get('/api/query/graph/<module>/<metric>')
def api_query_graph(module,metric):
  dt_start = api_dt_start(request)
  dt_end = api_dt_end(request)
  count = 5
  graph = query.graph_query(module, metric, count, dt_start, dt_end)
  return {"result": graph}

@get('/api/query/host/<hostname>/<module>/<metric>')
def api_query_host(hostname, module, metric):
  dt_start = api_dt_start(request)
  dt_end = api_dt_end(request)
  count = 5
  table = query.host_query(hostname, module, metric, count, dt_start, dt_end)
  return {"result": table}

if __name__ == '__main__':
  run (host='0.0.0.0', port=8082, debug=True,reloader=True)
