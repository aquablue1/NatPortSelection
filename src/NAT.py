from src.JobQueue import JobQueue
from src.PortPool import Port, PortPool

PORT_START = 1
PORT_END = 101


class nat(object):
    def __init__(self):
        self.queue = JobQueue()
        self.port_pool = PortPool(PORT_START, PORT_END)