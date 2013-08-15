import psutil
import os
import time

class Utilization():
  def __init__(self):
    n = psutil.net_io_counters()
    self.old_net = n.bytes_sent + n.bytes_recv
    self.old_time = time.time()
  
  def load_avg(self):
    load_avg = os.getloadavg()[0]
    return load_avg

  def cpu_use(self):
    return psutil.cpu_percent(interval=0.2) 

  def net_use_now(self, interval=0.2):
    n = psutil.net_io_counters()
    old_net = n.bytes_sent + n.bytes_recv
    time.sleep(interval)
    n = psutil.net_io_counters()
    new_net = n.bytes_sent + n.bytes_recv
    dif_net = new_net - old_net
    use_rate = dif_net / interval 
    return use_rate

  def net_use_last(self):
    n = psutil.net_io_counters()
    new_net = n.bytes_sent + n.bytes_recv
    dif_net = new_net - self.old_net
    new_time = time.time()
    interval = new_time - self.old_time
    use_rate = dif_net / interval
    self.old_time = new_time
    self.old_net = new_net
    return use_rate

if __name__ == '__main__':
  ut = Utilization()
  while True:
    time.sleep(1)
    print ut.cpu_use()
    print ut.net_use_now() / 1024
    print ut.net_use_last() / 1024
