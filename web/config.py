#put common configuration used by server and scheduler here
import datetime

MEMCACHE_SERVER = 'localhost:11211'
IPERF_INTERVAL = 60
LISTEN_INTERVAL = 15
<<<<<<< HEAD
STATIC_ROOT='/home/mekpro/workspace/overlord/web/assets/'
#STATIC_ROOT='/root/overlord/web/assets/'
=======
DT_QUERY =  datetime.timedelta(minutes=180)
#STATIC_ROOT='/home/mekpro/workspace/overlord/web/assets/'
STATIC_ROOT='/root/overlord/web/assets/'
>>>>>>> 228bce8a35a5113b1a18754dd9d4af0d9ca12834

MONGO_SERVER = 'localhost'
MONGO_DB = 'overlord'
