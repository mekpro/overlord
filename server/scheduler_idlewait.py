import datetime
import pymongo
import logging

MEMCACHE_SERVER = 'localhost:11211'
IPERF_INTERVAL = 60
# LISTEN_INTERVAL = 


def load_hostlist():
    hostlist = mc.get('hostlist')
    if hostlist is None:
        hostlist = [
            '192.168.1.100',
            '192.168.1.101',
            '192.168.1.102',
            '192.168.1.103',
            '192.168.1.104',
        ]
        mc.set('hostlist', hostlist)
    return hostlist


def initialize():
    mc = memcache.Client(MEMCACHE_SERVER, debug=0)
    hostlist = load_hostlist()
    mc.set('hostlist', hostlist)
    for i in hostlist:
        for j in hostlist:
            mc.set("last_" + i + j, datetime.datetime.now())
            mc.set("status_" + i + j, "busy")


def getScheduledHost(host_i):
    hostlist = load_hostlist()
    scheduled_hosts = []
    # last_update = datetime.datetime.now()
    for host_j in hostlist:
        if host_j != host_i:
            last_j = mc.get('last_' + host_i + host_j)
            update_time = datetime.datetime.now() - datetime.datediff(seconds=15)
            if last_j < update_time:
                scheduled_hosts.append(host_j)
    return scheduled_hosts

