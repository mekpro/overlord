import datetime
from pymongo import MongoClient
import logging

import config

def hostlist():
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  result = []
  for host in conn.host.find():
    result.append(host["hostname"])
  return result

def hoststats():
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  result = []
  for host in conn.host.find():
    r = dict()
    r["hostname"] = host["hostname"]
    r["status"] = host["status"]
    result.append(r)
  return result

def flowlist(hostname):
  result = []
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  flows = conn.flow.find({'src' : hostname})
  for flow in flows:
    result.append(flow["dest"])
  return result

def flowstats(hostname):
  result = []
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  flows = conn.flow.find({'src' : hostname})
  for flow in flows:
    r = dict()
    r["src"] = flow["src"]
    r["dest"] = flow["dest"]
    r["last_iperf_dt"] = str(flow["last_iperf_dt"])
    r["last_ping_dt"] = str(flow["last_ping_dt"])
    result.append(r)
  return result

def host_tables(hostname, metric="ping", dt=None):
  table = list()
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  if dt is None:
    dt = datetime.datetime.now()
  src_host = conn.host.find_one({'hostname':hostname})
  dest_hosts = conn.host.find()
  for dest_host in dest_hosts:
    query = {'src': src_host['hostname'], 'dest': dest_host['hostname'], 'type':metric}
    value = conn["values"].find_one(query)
    if value is not None:
      if metric == 'ping':
        table.append({'dest': dest_host['hostname'], 'dt': value["dt"] ,'min': value["min"], 'max': value["max"], 'avg': value["avg"]})
      elif metric == 'iperf':
        table.append({'dest': dest_host['hostname'], 'dt': value["dt"] ,'bandwidth':value["bandwidth"]})
  return table

def host_query(src_hostname, module, metric, count, dt_start, dt_end):
  result = []
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  query = {
    'src' : src_hostname,
    'type' : module,
    'dt' : { '$gt' : dt_start, '$lte': dt_end },
  }
  rows = conn['values'].find(query)
  print rows.count()
  for row in rows:
    r = dict()
    r["dt"] = str(row["dt"])
    r["key"] = row["dest"]
    r["value"] = row[metric]
    result.append(r)
  return result

def graph_query(module, metric, count, dt_start, dt_end):
  result = dict()
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  hosts = hostlist()
  for src_host in hosts:
    results = host_query(src_host, module, metric, count, dt_start, dt_end)
    result[src_host] = results
  return result

def graph_force():
  graph = list()
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  for hostname in hostlist():
    node = {
            "id": hostname,
            "name": hostname,
            "data" : {
              "$color" : "#83548B",
              "$type" : "circle",
              "$dim" : 10
            },
            "adjacencies" : [hostname]
          }
    iperf_tables = host_tables(hostname, "iperf")
    for row in iperf_tables:
      adj = {
        "nodeTo": row["dest"],
        "nodeFrom": hostname,
        "data": {"$color": "#557EAA"},
        }
      node["adjacencies"].append(adj)
    graph.append(node)

  return graph

def graph_force_ref():
  graph = list()
  fe = { "adjacencies": [
              "fe", {
                "nodeTo": "c0",
                "nodeFrom": "fe",
                "data": {"$color": "#557EAA"}
              }, {
                "nodeTo": "c1",
                "nodeFrom": "fe",
                "data": {"$color": "#557EAA"}
              }
            ],
              "data" : {
                "$color" : "#83548B",
                "$type": "circle",
                "$dim": 10
              },
              "id": "fe",
              "name": "fe"
          }
  c0 = { "adjacencies": [
              "c0", {
                "nodeTo": "c1",
                "nodeFrom": "c0",
                "data": {"$color": "#557EAA"}
              }
              ],
              "data" : {
                "$color" : "#43548B",
                "$type": "circle",
                "$dim": 8
              },
              "id": "c0",
              "name": "c0"
          }
  c1 = { "adjacencies": [],
              "data" : {
                "$color" : "#43548B",
                "$type": "circle",
                "$dim": 8
              },
              "id": "c0",
              "name": "c0"
          }
  graph.append(fe)
  graph.append(c0)
  graph.append(c1)
  return graph

if __name__ == '__main__':
  dt_start = datetime.datetime.now() - datetime.timedelta(minutes=10)
  dt_end = datetime.datetime.now()

  print hostlist()
  print host_tables('fe', 'iperf', dt_start)
  print host_query('fe', 'iperf', 'bandwidth', 10, dt_start, dt_end)
  print graph_query('iperf', 'bandwidth', 5, dt_start, dt_end)
#  print graph_force()

