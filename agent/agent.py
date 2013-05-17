import sys
import os
import json
import time
import requests
import logging
import config
from lib.daemon import Daemon

from lib import iperfshell
from lib import pingshell

logger = logging.getLogger('Agent')
hdlr = logging.FileHandler('/tmp/overlord_agent.log')
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

def spawn_iperf_server(port=None):
  os.popen('killall -9 -v iperf')
  output = os.system('/usr/bin/iperf -s -D &')
  print 'iperf started'

class Agent(Daemon):
  def run(self):
    spawn_iperf_server()
    headers = {'content-type': 'application/json'}
    request = dict()
    request["hostname"] = config.AGENT_HOSTNAME 
    request["authkey"] = 'none'
    request["state"] = 'idle'
    request["results"] = []
    while True:
      logger.info('connecting to %s with %s' %(config.SERVER, json.dumps(request)))
      response = requests.post(config.SERVER, data=json.dumps(request), headers=headers)
      request["results"] = []
      logger.info('response: %s' %(response.json()))
      response = response.json()
      jobs = response["jobs"]
      if len(jobs) == 0:
        logger.info('Sleeping ...')
        time.sleep(config.INTERVAL)
      else:
        for job in jobs:
          result = dict()
          result['src'] = config.AGENT_HOSTNAME
          result['dest'] = job["hostname"]
          if job['type'] == 'iperf':
            result['type'] = 'iperf'
            tmp = iperfshell.run_iperf(job["hostname"])
            values = iperfshell.parse_iperf(tmp)
          elif job['type'] == 'ping':
            result['type'] = 'ping'
            tmp = pingshell.run_ping(job["hostname"])
            values = pingshell.parse_ping(tmp)
          else:
            values = None
          result["values"] = values
          request["results"].append(result)

if __name__ == '__main__':
  daemon = Agent(config.PID_FILE)
  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      daemon.run()
      #daemon.start()
    elif 'stop' == sys.argv[1]:
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      daemon.restart()
    else:
      print "Unknown command"
      sys.exit(2)
    sys.exit(0)
  else:
    print "usage: %s start|stop|restart" % sys.argv[0]
    sys.exit(2)

