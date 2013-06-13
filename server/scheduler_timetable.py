import datetime
from pymongo import MongoClient
# import pymongo
# import logging
# import random

import common
import config


def gen_timetable():
    """
    timetable.append(('src_host', 'dest_host', 'type', 'hour', 'minute'))
    """
    timetable = list()
    hostlist = common.load_hostlist()
    dt = datetime.datetime.now()
    for host1 in hostlist:
        for host2 in hostlist:
            timetable.append({
                'src': host1,
                'dest': host2,
                'type': 'iperf',
                'hour': dt.hour,
                'minute': dt.minute
            })
            dt += datetime.timedelta(minutes=1)
    return timetable


def initialize():
    """
    Do neccessary data initialize for this scheduler
    Initialized data is stored in DB for access
    """
    timetable = gen_timetable()
    conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
    conn["timetable"].drop()
    for row in timetable:
        conn["timetable"].insert(row)


def getJobForHost(src_hostname):
    """
    Return job list of job ([{'type','hostname'}]) for the requested host.
    Return blank list if no job is currently needed.
    """
    result = []
    conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
    timetable = conn["timetable"].find()
    # hostlist = common.load_hostlist()
    dt = datetime.datetime.now()
    for row in timetable:
        if (src_hostname == row['src']):
            if (row['hour'] == dt.hour) and (row['minute'] == dt.minute):
                result.append({'type': row['type'], 'hostname': row['dest']})
    return result


if __name__ == '__main__':
    initialize()
    print(getJobForHost('fe'))
