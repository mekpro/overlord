import datetime
from pymongo import MongoClient

import common

def hostlist():
  conn = MongoClient(common.MONGO_SERVER)[common.MONGO_DB]
  hostlist = []
  for host in conn.host.find():
    hostlist.append(host["hostname"])
  return hostlist

def host_tables(hostname, metric="ping", dt=None):
  table = list()
  conn = MongoClient(common.MONGO_SERVER)[common.MONGO_DB]
  if dt is None:
    dt = datetime.datetime.now()
  print hostname
  src_host = conn.host.find_one({'hostname':hostname})
  dest_hosts = conn.host.find()
  for dest_host in dest_hosts:
    query = {'src': src_host['hostname'], 'dest': dest_host['hostname']}
    value = conn["values"].find_one(query)
    if value is not None:
      table.append({'dest': dest_host['hostname'], 'dt': value["dt"] ,'values':value["values"]})
  return table

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
