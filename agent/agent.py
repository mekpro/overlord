import sys
import os
import json
import time
import requests
import logging
from daemon import Daemon

from lib import iperfshell
from lib import pingshell

SERVER = "http://localhost:8081/listen"
INTERVAL = 15

def spawn_iperf_server(port=None):
  os.popen('killall -9 -v iperf')
  output = os.popen('/usr/bin/iperf -s -D | grep ID').read()
#  process_id = int(output.split()[-1])
  return 0

class Agent(Daemon):
  def run(self):
    logger = logging.getLogger('Agent')
    hdlr = logging.FileHandler('/tmp/overlord_agent.log')
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    iperf_pid = spawn_iperf_server()
    headers = {'content-type': 'application/json'}
    request = dict()
    request["hostname"] = 'myhostname'
    request["authkey"] = 'myauthkey'
    request["state"] = 'idle'
    request["results"] = []
    while True:
      logger.info('connecting to %s with %s' %(SERVER,json.dumps(request)))
      response = requests.post(SERVER, data=json.dumps(request), headers=headers)
      request["results"] = []
      logger.info('response: %s' %(response.json()))
      response = response.json()
      jobs = response["jobs"]
      if len(jobs) == 0:
        logger.info('Sleeping ...')
        time.sleep(INTERVAL)
      else:
        for job in jobs:
          if job['type'] == 'iperf':
            tmp = iperfshell.run_iperf(job["hostname"])
            result = iperfshell.parse_iperf(tmp)
          elif job['type'] == 'ping':
            tmp = pingshell.run_ping(job["hostname"])
            result = pingshell.parse_ping(tmp)
          else:
            result = None
          request["results"].append(result)

if __name__ == '__main__':
  daemon = Agent('/tmp/overlord_agent.pid')
  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      #daemon.run()
      daemon.start()
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

