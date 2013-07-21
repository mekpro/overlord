import os

def run_iperf(hostname, port=None):
  iperf_cmd = "iperf -y c "
  iperf_cmd += "-c %s" %str(hostname)
  if port is not None:
    iperf_cmd += " -p %s" %str(port)
  print iperf_cmd
  result = os.popen(iperf_cmd).read()
  return result

def parse_iperf(iperf_result):
# 20130510202555,127.0.0.1,50469,127.0.0.1,5001,3,0.0-10.0,46052278272,36841295787
  numbers = iperf_result.split(",")
  bandwidth = int(numbers[7])
  result = dict()
  result["bandwidth"] = bandwidth
  return result

if __name__ == '__main__':
  result = run_iperf('localhost')
  print result
  bw = parse_iperf(result)
  print bw
