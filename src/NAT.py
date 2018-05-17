import random
from src.JobQueue import JobQueue
from src.PortPool import PortPool
from src.LogInfo import write_error, write_runtimeInfo

PORT_START = 1
PORT_END = 200
# PORT_END = 200        # This case failed because it needs more than 200 ports



class NAT(object):
    def __init__(self, job=None):
        self.queue = JobQueue(job)
        self.port_pool = PortPool(PORT_START, PORT_END)
        self.next_port = PORT_START



    def alg1_random_choose(self):
        rand =random.choice(self.port_pool.pool_free)
        # print(rand)
        if rand == None:
            write_error("Error, no available port in PoolFree")
        return rand

    def alg1_port_assign(self, job):
        port = self.alg1_random_choose()
        self.port_pool.do_setInuse((port, job))

    def alg2_increasing_choose(self):
        while True:
            port = self.port_pool.find_port(self.next_port)
            if port is None:
                self.next_port = PORT_START
                continue
            elif port.status != 0:
                write_runtimeInfo("Port Num %d current in use or in cooldown, switch to next" % self.next_port)
                if self.next_port<PORT_END-1:
                    self.next_port=self.next_port+1
                else:
                    self.next_port=PORT_START
            else:
                self.next_port += 1
                return port

    def alg2_port_assign(self, job):
        port = self.alg2_increasing_choose()
        self.port_pool.do_setInuse((port, job))

if __name__ == '__main__':
    nat = NAT()
    print(nat.alg1_random_choose())