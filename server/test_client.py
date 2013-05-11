import requests
import json

request = dict()
request['hostname'] = 'myhostname'
request['authkey'] = 'myauthkey'
request['state'] = 'idle'
request['results'] = []

server = 'http://localhost:8081/listen'
headers = {'content-type': 'application/json'}

r = requests.post(server, data=json.dumps(request), headers=headers)
print r.text
