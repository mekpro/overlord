import os

def run_ping(hostname, count=4, interval=1, timeout=5):
  ping_cmd = 'ping %s -c %s -i %s -w %s' % (hostname, str(count),str(interval),str(timeout))
  ping_cmd += '| grep avg'
  print ping_cmd
  result = os.popen(ping_cmd).read()
  return result

def parse_ping(ping_result):
# 'rtt min/avg/max/mdev = 4.306/4.672/5.333/0.402 ms\n'
  numbers = ping_result.split(' = ')[1]
  numbers = numbers.split(' ')[0]
  numbers = numbers.split('/')
  result = dict()
  result['min'] = float(numbers[0])
  result['avg'] = float(numbers[1])
  result['max'] = float(numbers[2])
  result['mdev'] = float(numbers[3])
  return result

if __name__ == '__main__':
  st_result = run_ping('localhost',20,1,20);
  i = parse_ping(st_result)
  print i

