import requests
import json

request = dict()
request['hostname'] = 'myhostname'
request['authkey'] = 'myauthkey'
request['state'] = 'idle'
request['results'] = []
result1 = {
    'type': 'iperf',
    'dest': 'yourhost',
    'values': {
        'bandwidth': 10000
    }
}
request['results'].append(result1)

server = 'http://localhost:8081/listen'
headers = {'content-type': 'application/json'}

r = requests.post(server, data=json.dumps(request), headers=headers)
print(r.text)
