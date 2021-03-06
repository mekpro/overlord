#put common configuration used by server and scheduler here
import datetime

MONGO_SERVER = 'localhost'
MONGO_DB = 'overlord'

IPERF_INTERVAL = datetime.timedelta(minutes=10)
IPERF_HARD_INTERVAL = datetime.timedelta(minutes=20)
PING_INTERVAL = datetime.timedelta(minutes=1)
LISTEN_INTERVAL = 15
STATE_TIMEOUT_INTERVAL = datetime.timedelta(minutes=60)
STATE_SAMPLING_INTERVAL = 60

ENABLE_HOSTGROUP = True
ENABLE_HOSTBUSY = True
MAX_RUNNING = 16
