#put common configuration used by server and scheduler here
import datetime

MEMCACHE_SERVER = 'localhost:11211'
IPERF_INTERVAL = 60
LISTEN_INTERVAL = 15
DT_QUERY =  datetime.timedelta(minutes=180)
#STATIC_ROOT='/home/mekpro/workspace/overlord/web/assets/'
STATIC_ROOT='/root/overlord/web/assets/'

MONGO_SERVER = 'localhost'
MONGO_DB = 'overlord'
