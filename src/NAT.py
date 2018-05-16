import random
from src.JobQueue import JobQueue
from src.PortPool import Port, PortPool


PORT_START = 1
PORT_END = 101


class nat(object):
    def __init__(self):
        self.queue = JobQueue()
        self.port_pool = PortPool(PORT_START, PORT_END)



    def alg1_random_choose(self):
        rand =random.choice(self.port_pool.pool_free)
        print(rand)
        return rand