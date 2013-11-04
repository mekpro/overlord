import datetime
from pymongo import MongoClient
import logging
import time
from bson.code import Code

import config

def dt_to_timestamp(dt):
  return time.mktime(dt.timetuple())

def dt_from_timestamp(timestamp):
  return datetime.datetime.fromtimestamp(timestamp)

def parse_form_dt(dt_string):
  dt_format = '%d/%m/%Y %H:%M:%S'
  return datetime.datetime.strptime(dt_string, dt_format)

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

def hostinfo(hostname):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  result = {}
  host = conn.host.find_one({'hostname': hostname})
  for k,v in host.items():
    if k != '_id':
      result[k] = str(v)
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
    r["last_iperf_dt"] = dt_to_timestamp(flow["last_iperf_dt"])
    r["last_ping_dt"] = dt_to_timestamp(flow["last_ping_dt"])
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
    value = conn["values"].find(query).sort([('dt',-1)])
    if value.count() > 0:
      v = value[0]
      if metric == 'ping':
        table.append({'dest': dest_host['hostname'], 'dt': v["dt"] ,'min': v["min"], 'max': v["max"], 'avg': v["avg"]})
      elif metric == 'iperf':
        table.append({'dest': dest_host['hostname'], 'dt': v["dt"] ,'bandwidth':v["bandwidth"]})
  return table

def host_query(src_hostname, module, metric, count, dt_start, dt_end):
  result = dict()
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  query = {
    'src' : src_hostname,
    'type' : module,
    'dt' : { '$gt' : dt_start, '$lte': dt_end },
  }
  rows = conn['values'].find(query)
  print rows.count()
  for row in rows:
    if row["dest"] not in result:
      result[row["dest"]] = list()
    r = (dt_to_timestamp(row["dt"]), row[metric])
    result[row["dest"]].append(r)

  return result


def host_aggregate(src_hostname, module, metric, dt_start, dt_end):
  result = dict()
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  result = conn["values"].aggregate([
    {"$match": {"src": src_hostname, "type": module}},
    {"$group": {"_id": "null",
      "count" : {"$sum" : 1},
      "sum" : { "$sum" : "$"+metric},
      "avg" : { "$avg" : "$"+metric},
      "min" : { "$min" : "$"+metric},
      "max" : { "$max" : "$"+metric},
      }
    },
  ])

  return result


def host_mapreduce(src_hostname, module, metric, dt_start, dt_end):
  result = dict()
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  mapcode = Code("""
    function () {
      var dt = new Date(this.dt);
      emit(this.dest, {
        sum: this.metric,
        min: this.metric,
        max: this.metric,
        count: 1,
        diff: 0,
        last_dt: dt
      });
    }
    """.replace("metric", metric))
  reducecode = Code("""
  function (key, values) {
    var a = values[0]; // will reduce into here
    for (var i=1; i < values.length; i++){
        var b = values[i]; // will merge 'b' into 'a'
        // temp helpers
        var delta = a.sum/a.count - b.sum/b.count; // a.mean - b.mean
        var weight = (a.count * b.count)/(a.count + b.count);
        // do the reducing
        a.diff += b.diff + delta*delta*weight;
        a.sum += b.sum;
        a.count += b.count;
        a.min = Math.min(a.min, b.min);
        a.max = Math.max(a.max, b.max);
        if (a.last_dt < b.last_dt){
          a.last_dt = b.last_dt;
        }
    }
    return a;
}
""")
  finalizecode = Code("""
  function(key, value) {
    value.avg = value.sum / value.count;
    value.variance = value.diff / value.count;
    value.stddev = Math.sqrt(value.variance);
    return value;
}
""")
  query = {
    'src' : src_hostname,
    'type' : module,
    'dt' : { '$gt' : dt_start, '$lte': dt_end },
  }
  mr_result = conn.values.map_reduce(mapcode, reducecode, "myresult", query=query, finalize=finalizecode)
  # do a little transpose
  for r in list(mr_result.find()):
    result[r["_id"]] = r["value"]
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
    dest_list = flowlist(hostname)
    for dest in dest_list:
      adj = {
        "nodeTo": dest,
        "nodeFrom": hostname,
        "data": {"$color": "#557EAA"},
        }
      node["adjacencies"].append(adj)
    graph.append(node)

  return graph

if __name__ == '__main__':
  dt_start = datetime.datetime.now() - datetime.timedelta(minutes=1700)
  dt_end = datetime.datetime.now()

#  print hostlist()
#  print host_tables('fe', 'iperf', dt_start)
#  print host_query('fe', 'iperf', 'bandwidth', 10, dt_start, dt_end)
#  print graph_query('iperf', 'bandwidth', 5, dt_start, dt_end)
#  print host_aggregate('fe', 'iperf', 'bandwidth', dt_start, dt_end)
  print host_mapreduce('fe', 'iperf', 'bandwidth', dt_start, dt_end)


#  print graph_force()

