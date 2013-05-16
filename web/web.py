import datetime
import bottle
from bottle import route, run, request, template
from bottle import static_file
from pymongo import MongoClient
import json
import logging

import query
import common

@route('/assets/<filepath:path>')
def server_static(filepath):
  return static_file(filepath, root='/home/mekpro/workspace/overlord/web/assets')

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
  return template('host_template', last_update=last_update)

if __name__ == '__main__':
  run (host='localhost', port=8082, debug=True,reloader=True)
