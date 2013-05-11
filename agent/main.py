import os
import json
import time
import requests
from lib import iperfshell
from lib import pingshell

SERVER = "http://localhost:8081/listen"
INTERVAL = 15

def spawn_iperf_server(port=None):
  os.system('/usr/bin/iperf -s &')

if __name__ == '__main__':
  spawn_iperf_server()
  headers = {'content-type': 'application/json'}
  request = dict()
  request["hostname"] = 'myhostname'
  request["authkey"] = 'myauthkey'
  request["state"] = 'idle'
  request["results"] = []
  while True:
    response = requests.post(SERVER, data=json.dumps(request), headers=headers)
    request["results"] = []
    response = response.json()
    jobs = response["jobs"]
    if len(jobs) == 0:
      time.sleep(INTERVAL)
    else:
      for job in :
        if job['type'] == 'iperf':
          tmp = iperfshell.run_iperf(job["hostname"])
          result = iperfshell.parse_iperf(tmp)
        elif job['type'] == 'ping':
          tmp = pingshell.run_ping(job["hostname"])
          result = pingshell.parse_ping(tmp)
        else:
          result = None
        request["results"].append(result)
