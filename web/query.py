import datetime
from pymongo import MongoClient

import common

def hostlist():
  conn = MongoClient(common.MONGO_SERVER)[common.MONGO_DB]
  hostlist = []
  for host in conn.host.find():
    hostlist.append(host["hostname"])
  return ['fe','c0','c1']

def host_tables(hostname, metric="ping"):
  conn = MongoClient(common.MONGO_SERVER)[common.MONGO_DB]
  host = conn.host.findOne(hostname=hostname)
  if metric == 'ping':
    pass
  elif metric == 'iperf':
    pass

def graph():
  conn = MongoClient(common.MONGO_SERVER)[common.MONGO_DB]
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
