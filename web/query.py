import datetime
from pymongo import MongoClient
import logging

import config

def hostlist():
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  hostlist = []
  for host in conn.host.find():
    hostlist.append(host["hostname"])
  return hostlist

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
    logging.error("%s %s %s" %(src_host['hostname'], dest_host['hostname'], str(value)))
    if value is not None:
      if metric == 'ping':
        table.append({'dest': dest_host['hostname'], 'dt': value["dt"] ,'min': value["min"], 'max': value["max"], 'avg': value["avg"]})
      elif metric == 'iperf':
        table.append({'dest': dest_host['hostname'], 'dt': value["dt"] ,'bandwidth':value["bandwidth"]})
  return table

def graph():
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


def graph_ref():
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
