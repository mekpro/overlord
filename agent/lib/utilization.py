import psutil
import time

class Utilization():
  def cpu_use(self):
    return psutil.cpu_percent(interval=0.2) 

  def net_use(self, interval=0.1):
    n = psutil.net_io_counters()
    old_net = n.bytes_sent + n.bytes_recv
    time.sleep(interval)
    n = psutil.net_io_counters()
    new_net = n.bytes_sent + n.bytes_recv
    dif_net = new_net - old_net
    use_rate = dif_net / interval 
    return use_rate

if __name__ == '__main__':
  ut = Utilization()
  while True:
    time.sleep(1)
    print ut.cpu_use()
    print ut.net_use() / 1024
