import random
from src.JobQueue import JobQueue
from src.PortPool import Job, PortPool
from src.LogInfo import write_error, write_runtimeInfo

PORT_START = 49152
PORT_END = 65535
# PORT_START = 1
# PORT_END = 300
GAP_BETWEEN_DIFF_REJ = 0.23
GAP_BETWEEN_REJP = 0.65
GAP_BETWEEN_REJQ = 0.1




# PORT_END = 200        # This case failed because it needs more than 200 ports



class NAT(object):
    def __init__(self, job=None):
        self.queue = JobQueue(job)
        self.port_pool = PortPool(PORT_START, PORT_END)
        self.next_port = PORT_START



    def alg1_random_choose(self):
        rand = random.choice(self.port_pool.pool_free)
        # print(rand)
        if rand == None:
            write_error("Error, no available port in PoolFree.")
        return rand

    def alg1_port_assign(self, job):
        port = self.alg1_random_choose()
        self.port_pool.do_setInuse((port, job))

    def find_next_port(self):
        if self.next_port < PORT_END-1:
            return self.next_port+1
        else:
            return PORT_START

    def alg2_increasing_choose(self):
        while True:
            port = self.port_pool.find_port(self.next_port)
            if port is None:
                self.next_port = PORT_START
                continue
            elif port.status != 0:
                write_runtimeInfo("Port Num %d current in use or in cooldown, switch to next." % self.next_port)
                self.next_port = self.find_next_port()
            else:
                self.next_port = self.find_next_port()
                return port

    def alg2_port_assign(self, job):
        port = self.alg2_increasing_choose()
        self.port_pool.do_setInuse((port, job))

    def alg3_min_choose(self):
        chosen_port = min(port.port_num for port in self.port_pool.pool_free)
        return self.port_pool.find_port(chosen_port)

    def alg3_port_assign(self, job):
        port = self.alg3_min_choose()
        self.port_pool.do_setInuse((port, job))

    def alg4_follow_orig(self, job):
        chosen_port_num = job.origPort
        chosen_port = self.port_pool.find_port(chosen_port_num)
        if chosen_port is None:
            chosen_port = random.choice(self.port_pool.pool_free)
            return chosen_port
        elif chosen_port.status != 0:
            write_runtimeInfo("Port Num %d current in use or in cooldown, switch to random." % self.next_port)
            chosen_port = random.choice(self.port_pool.pool_free)
            return chosen_port
        else:
            return chosen_port

    def alg4_port_assign(self, job):
        port = self.alg4_follow_orig(job)
        self.port_pool.do_setInuse((port, job))

    def alg5_sticky_increase(self, job):
        self.next_port = job.origPort
        chosen_port = self.port_pool.find_port(self.next_port)
        while True:
            if chosen_port is None:
                self.next_port = PORT_START
                chosen_port = self.port_pool.find_port(self.next_port)
            elif chosen_port.status != 0:
                write_runtimeInfo("Port Num %d current in use or in cooldown, switch to Next One (Increasing)." % self.next_port)
                self.next_port = self.find_next_port()
                chosen_port = self.port_pool.total_port_dict[self.next_port]
            else:
                return chosen_port

    def alg5_port_assign(self, job):
        port = self.alg5_sticky_increase(job)
        self.port_pool.do_setInuse((port, job))

    def alg6_port_assign(self, job):
        if job.endStatus == "REJPM1":
            rand = random.randint(0, 50)
            if rand != 1:
                new_job_ph1 = Job(job.job_str)
                new_job_ph1.endStatus = "REJPH1"
                new_job_ph1.ts += GAP_BETWEEN_DIFF_REJ
                new_job_ph1.origPort += 1

                new_job_pm1 = Job(job.job_str)
                new_job_pm1.endStatus = "REJPM1"
                new_job_pm1.ts += (GAP_BETWEEN_DIFF_REJ + GAP_BETWEEN_REJP)
                new_job_pm1.origPort += 1

                new_job_pe1 = Job(job.job_str)
                new_job_pe1.endStatus = "REJPE1"
                new_job_pe1.ts += (GAP_BETWEEN_DIFF_REJ + GAP_BETWEEN_REJP*2)
                new_job_pe1.origPort += 1

                self.queue.insert_urgent_job(new_job_ph1)
                self.queue.insert_urgent_job(new_job_pm1)
                self.queue.insert_urgent_job(new_job_pe1)

        elif job.endStatus == "REJPE2":
            rand = random.randint(0, 50)
            if rand != 1:
                new_job_ph1 = Job(job.job_str)
                new_job_ph1.endStatus = "REJPH2"
                new_job_ph1.ts += GAP_BETWEEN_DIFF_REJ
                new_job_ph1.increase_origPort(1)

                new_job_pm1 = Job(job.job_str)
                new_job_pm1.endStatus = "REJPM2"
                new_job_pm1.ts += (GAP_BETWEEN_DIFF_REJ + GAP_BETWEEN_REJP)
                new_job_pm1.increase_origPort(1)

                new_job_pe1 = Job(job.job_str)
                new_job_pe1.endStatus = "REJPE2"
                new_job_pe1.ts += (GAP_BETWEEN_DIFF_REJ + GAP_BETWEEN_REJP * 2)
                new_job_pe1.increase_origPort(1)

                self.queue.insert_urgent_job(new_job_ph1)
                self.queue.insert_urgent_job(new_job_pm1)
                self.queue.insert_urgent_job(new_job_pe1)
        elif job.endStatus == "REJQ":
            new_job_q = Job(job.job_str)
            new_job_q.endStatus = "REJQ"
            new_job_q.ts += GAP_BETWEEN_REJQ
            new_job_q.increase_origPort(1)

        port = self.alg5_sticky_increase(job)
        self.port_pool.do_setInuse((port, job))


if __name__ == '__main__':
    nat = NAT()
    print(nat.alg1_random_choose())