import random
from src.JobQueue import JobQueue
from src.PortPool import PortPool
from src.LogInfo import write_error


PORT_START = 1
PORT_END = 500


class NAT(object):
    def __init__(self, job=None):
        self.queue = JobQueue(job)
        self.port_pool = PortPool(PORT_START, PORT_END)



    def alg1_random_choose(self):
        rand =random.choice(self.port_pool.pool_free)
        # print(rand)
        if rand == None:
            write_error("Error, no available port in PoolFree")
        return rand

    def alg1_port_assign(self, job):
        port = self.alg1_random_choose()
        self.port_pool.do_setInuse((port, job))



if __name__ == '__main__':
    nat = NAT()
    print(nat.alg1_random_choose())