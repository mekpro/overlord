#config file for overlord agent

AGENT_HOSTNAME = "fe"
AGENT_AUTHKEY = "none"
SERVER_LISTEN = "http://fe:8081/listen"
SERVER_GETJOBS = "http://fe:8081/getjobs"
INTERVAL = 15
PID_FILE = "/tmp/overlord_agent.pid"

CPU_BUSY = 50
NET_BUSY = 10240000
