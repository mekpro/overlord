#put common configuration used by server and scheduler here
import datetime

MEMCACHE_SERVER = 'localhost:11211'
IPERF_INTERVAL = datetime.timedelta(minutes=5)
IPERF_HARD_INTERVAL = datetime.timedelta(minutes=15)
PING_INTERVAL = datetime.timedelta(minutes=1)
LISTEN_INTERVAL = 15
STATE_TIMEOUT_INTERVAL = datetime.timedelta(minutes=3)
STATE_SAMPLING_INTERVAL = 60

MONGO_SERVER = 'localhost'
MONGO_DB = 'overlord'
