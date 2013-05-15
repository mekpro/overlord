import datetime
import bottle
from bottle import route, run, request, template
from bottle import static_file
from pymongo import MongoClient

import common

def get_hostlist():
  #  conn = MongoClient(common.MONGO_SERVER)[common.MONGO_DB]
  return ['fe','c0','c1']

@route('/assets/<filepath:path>')
def server_static(filepath):
  return static_file(filepath, root='/home/mekpro/workspace/overlord/web/assets')

@route('/index')
def index():
  last_update = datetime.datetime.now()
  return template('index_template', last_update=last_update)

@route('/host')
def host():
  return template('host_template', last_update=last_update)

if __name__ == '__main__':
  run (host='localhost', port=8082, debug=True,reloader=True)
