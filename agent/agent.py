import sys
import os
import json
import time
import requests
import logging
import config
from lib.daemon import Daemon
from lib.utilization import Utilization

from lib import netperfshell
from lib import pingshell

logger = logging.getLogger('Agent')
hdlr = logging.FileHandler('/tmp/overlord_agent.log')
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

def spawn_iperf_server(port=None):
  #os.popen('killall -9 -v iperf')
  #output = os.system('/usr/bin/iperf -s -D &')
  os.popen('killall -9 -v netserver')
  output = os.system('netserver')
  print 'netperf server started'

def do_jobs(jobs):
  results = []
  for job in jobs:
    logger.error('Working with %s', str(job))
    result = dict()
    result['src'] = config.AGENT_HOSTNAME
    result['dest'] = job["hostname"]
    if job['type'] == 'iperf':
      tmp = netperfshell.run_iperf(job["hostname"])
      logger.error('netperf output :' +tmp);
      if not tmp == '':
        values = netperfshell.parse_iperf(tmp)
        result['type'] = 'iperf'
      else: 
        values = {}
        result['type'] = 'failed'
    elif job['type'] == 'ping':
      tmp = pingshell.run_ping(job["hostname"])
      values = pingshell.parse_ping(tmp)
      result['type'] = 'ping'
    else:
      values = {}
    for k,v in values.iteritems():
      result[k] = v
    results.append(result)
  return results

class Agent(Daemon):
  def run(self):
    spawn_iperf_server()
    utilize = Utilization()
    headers = {'content-type': 'application/json'}
    request = {
      "hostname": config.AGENT_HOSTNAME,
      "authkey": 'none',
    }
    while True:
      try:
        # get my status
        # if busy
        #   send busy
        #   short sleep
        # if idle
        #   send idle
        #   get jobs
        #   do jobs or idle
        # !!!
        # must change server request from listen to listen/getjobs
        request["results"] = []
        cpu_use = utilize.cpu_use()
        net_use_now = utilize.net_use_now()
        net_use_last = utilize.net_use_last()
        load_avg = utilize.load_avg()
        request["results"].append({
            'type' : 'utilization',
            'dest' : config.AGENT_HOSTNAME,
            'cpu' : cpu_use,
            'net' : net_use_last,
            'loadavg' : load_avg,
        })
        if cpu_use > config.CPU_BUSY or net_use_now > config.NET_BUSY:
          request["status"] = "busy"
          response = requests.post(config.SERVER_LISTEN, data=json.dumps(request), headers=headers)
          time.sleep(config.INTERVAL)
        else:
          request["status"] = "idle"
          requests.post(config.SERVER_LISTEN, data=json.dumps(request), headers=headers)
          response = requests.post(config.SERVER_GETJOBS, data=json.dumps(request), headers=headers)
          logger.info('response: %s' %(response.json()))
          jobs = response.json()["jobs"]
          if len(jobs) == 0:
            logger.error('Sleeping ...')
            time.sleep(config.INTERVAL)
          else:
            logger.info('jobs: %s' %(str(jobs)))
            request["results"] = do_jobs(jobs)
            request["status"] = "idle"
            response = requests.post(config.SERVER_LISTEN, data=json.dumps(request), headers=headers)
      except (requests.Timeout):
        logging.error("Connection to "+config.SERVER_LISTEN+" timeout")
        time.sleep(config.INTERVAL)
 

if __name__ == '__main__':
  daemon = Agent(config.PID_FILE)
  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      daemon.start()
    elif 'run' == sys.argv[1]:
      daemon.run()
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

