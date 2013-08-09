import psutil
import time

class Utilization():
  def __init__(self):
    n = psutil.net_io_counters()
    self.last_net = n.bytes_sent + n.bytes_recv
    self.last_time = time.time()

  def cpu_time(self):
    return psutil.cpu_percent(interval=0.2) 

  def net_use_rate(self):
    n = psutil.net_io_counters()
    cur_net = n.bytes_sent + n.bytes_recv
    dif_net = cur_net - self.last_net
    time_dif = time.time() - self.last_time
    use_rate = dif_net / time_dif
    self.last_net = cur_net
    self.last_time = time.time()
    return use_rate

if __name__ == '__main__':
  ut = Utilization()
  while True:
    time.sleep(1)
    print ut.cpu_time()
    print ut.net_use_rate() / 1024000
