import bottle
from bottle import get, post, route, run, request, template
from bottle import static_file
from pymongo import MongoClient
import datetime
import json
import logging

import query
import config

def get_dt_start(request):
  if 'dt_start' not in request.GET:
    dt_start = datetime.datetime.now() - config.DT_QUERY
  else:
    dt_start = query.dt_from_timestamp(float(request.GET['dt_start']))
  return dt_start

def get_dt_end(request, dt_start):
  if 'dt_end' not in request.GET:
    dt_end = dt_start + config.DT_QUERY
  else:
    dt_end = query.dt_from_timestamp(float(request.GET['dt_end']))
  return dt_end

def post_dt_start(request):
  if request.forms.get('dt_start') == '':
    dt_start = datetime.datetime.now() - config.DT_QUERY
  else:
    dt_start = query.parse_form_dt(request.forms.get('dt_start'))
  return dt_start

def post_dt_end(request, dt_start):
  if request.forms.get('dt_end') == '':
    dt_end = dt_start + config.DT_QUERY
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
  dt_start = datetime.datetime.now() - config.DT_QUERY
  dt_end = datetime.datetime.now()
  hostlist = query.hostlist()
  ping_table = query.host_mapreduce(hostname, 'ping', 'avg', dt_start, dt_end)
  iperf_table = query.host_mapreduce(hostname, 'iperf', 'bandwidth', dt_start, dt_end)
  logging.error(iperf_table)
  return template('host_template', title=hostname, hostname=hostname, hostlist=hostlist, last_update=last_update, dt_start=query.dt_to_timestamp(dt_start), dt_end=query.dt_to_timestamp(dt_end), ping_table=ping_table, iperf_table=iperf_table)

@post('/host/<hostname>')
def host_view_post(hostname):
  dt_start = post_dt_start(request)
  dt_end = post_dt_end(request, dt_start)
  last_update = datetime.datetime.now()
  hostlist = query.hostlist()
  ping_table = query.host_mapreduce(hostname, 'ping', 'avg', dt_start, dt_end)
  iperf_table = query.host_mapreduce(hostname, 'iperf', 'bandwidth', dt_start, dt_end)
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

@get('/api/hostinfo/<hostname>')
def api_hoststats(hostname):
  hostinfo = query.hostinfo(hostname)
  return {"result" : hostinfo}

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
  dt_start = get_dt_start(request)
  dt_end = get_dt_end(request)
  count = 5
  graph = query.graph_query(module, metric, count, dt_start, dt_end)
  return {"result": graph}

@get('/api/query/host/<hostname>/<module>/<metric>')
def api_query_host(hostname, module, metric):
  dt_start = get_dt_start(request)
  dt_end = get_dt_end(request, dt_start)
  count = 5
  table = query.host_query(hostname, module, metric, count, dt_start, dt_end)
  return {"result": table}

@get('/api/aggregate/host/<hostname>/<module>/<metric>')
def api_aggregate_host(hostname, module, metric):
  dt_start = get_dt_start(request)
  dt_end = get_dt_end(request, dt_start)
  table = query.host_mapreduce(hostname, module, metric, dt_start, dt_end)
  for k,v in table.items():
    table[k]['last_dt'] = query.dt_to_timestamp(table[k]['last_dt'])
  return {"result": table}

#@get('/api/config/addhost')

#@get('/api/config/delhost')

#@get('/api/config/addflow')

#@get('/api/config/delflow')

if __name__ == '__main__':
  run (host='0.0.0.0', port=8082, debug=True,reloader=True)
