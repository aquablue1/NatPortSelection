from src.JobQueue import Job
from src.LogInfo import write_error, write_runtimeInfo, write_output

DEFAULT_COOLDOWN_TIME = 10


class Port(object):
    def __init__(self, port_num):
        """
        Port object, represents a port in a NAT
        Status: 0 - Free
                1 - Inuse
                2 - CoolDown
        :param port_num:
        """
        self.port_num = port_num
        self.status = 0
        self.using_left = 0
        self.cooldown_left = DEFAULT_COOLDOWN_TIME
        self.job = None

    def assign(self, job):
        if (self.status == 0):
            self.status = 1
            self.job = job
            self.job.status = 1
            self.job.realPort = self.port_num
            self.using_left = job.duration
            write_output("%f\t%d" % (self.job.ts, self.port_num))
            return True
        else:
            write_error("Unable to Assign, current status is %d." % self.status)
            return False

    def using(self, time_past):
        if (self.status == 1):
            self.using_left -= time_past
            if (self.using_left <= 0):
                self.status = 2
                self.using_left = 0
                self.job.status = 2
                write_runtimeInfo("Port %d Just Cool Down" % self.port_num)
                return True
            return False
        else:
            write_error("Unable to Using, current status is %d" % self.status)

    def cool_down(self, time_past):
        """
        Method for simulates the cool down process of a port
        Only if status==2 where cool down is legal
        If no timeslice left, the cooldown process ends and the
            status will be set as free.
        :param time_past:
        :return:
        """
        if (self.status == 2):
            self.cooldown_left -= time_past
            if (self.cooldown_left <= 0):
                self.status = 0
                self.cooldown_left = DEFAULT_COOLDOWN_TIME
                write_runtimeInfo("Port %d Just Set Free" % self.port_num)
                return True
            return False
        else:
            write_error("Unable to Cool Down, current status is %d" % self.status)

    def __str__(self):
        return "Port Number  %d, Current Status: %d" % (self.port_num, self.status)

    def __repr__(self):
        return "Port Number  %d, Current Status: %d" % (self.port_num, self.status)


class PortPool(object):
    def __init__(self, port_start, port_end):
        """
        Identify the start and the end of the useful ports in a NAT.
        Start is included and end is excluded
        :param port_start:
        :param port_end:
        """
        if (port_start<0 or port_end > 65536):
            write_error("Illegal Port Num Setting")
        if (port_start > port_end):
            write_error("PortStart larger than PortEnd")
            port_start, port_end = port_end, port_start

        self.total_port = []
        self.pool_free = []
        self.pool_inuse = []
        self.pool_cooldown = []
        for i in range(port_start, port_end):
            port_tmp = Port(i)
            self.total_port.append(port_tmp)

        self.init_nat()

    def __repr__(self):
        return "Len PoolFree %d, Len PoolInuse %d, Len PoolCooldown %d." % (len(self.pool_free),
                                                                            len(self.pool_inuse),
                                                                            len(self.pool_cooldown))

    def init_nat(self):
        for port in self.total_port:
            port.status = 0
            port.using_left = 0
            port.cooldown_left = DEFAULT_COOLDOWN_TIME
            self.pool_free.append(port)
        return True

    def get_Free(self):
        return self.pool_free

    def get_inuse(self):
        return self.pool_inuse

    def get_cooldown(self):
        return self.pool_cooldown

    def do_timepast(self, time_gap):
        """
        Simulate two jobs:
        1. reduce time slice for those already in use, check if they run out of time slice
        2. reduce time slice for those cool downing, check if they run out of time slice
        :param time_gap: The time just past, the smaller time_gap is, the more precise the simulation is.
        :return:
        """
        for port_inuse in self.pool_inuse:
            if (port_inuse.using(time_gap)):
                # Return true indicates this port runs of time slice.
                # Hence move it to PoolCoolDown
                self.pool_inuse.remove(port_inuse)
                if port_inuse.status == 2:
                    self.pool_cooldown.append(port_inuse)
                else:
                    write_error("Warning! port removed from PoolInuse but not moved to PoolCooldown")

        for port_cooldown in self.pool_cooldown:
            if (port_cooldown.cool_down(time_gap)):
                # Return true indicates this port already cool down.
                # Hence move it to PoolFree
                self.pool_cooldown.remove(port_cooldown)
                # port_cooldown.job = None
                if port_cooldown.status == 0:
                    self.pool_free.append(port_cooldown)
                else:
                    write_error("Warning! port removed from PoolCoolDown but not moved to PoolFree")

    def do_setInuse(self, tobe_pair):
        """
        Set the ports in tobe_used_list from PoolFree into PoolInuse.
        :param tobe_pair_list: list of the [ports, duration] list to be used right now.
        :return: status
        """

        tobe_port = tobe_pair[0]
        todo_job = tobe_pair[1]
        tobe_port.assign(todo_job)
        write_runtimeInfo("Assign Job %s to Port %d, duration %f" %(todo_job.jobID,
                                                        tobe_port.port_num,
                                                        todo_job.duration))
        self.pool_free.remove(tobe_port)
        self.pool_inuse.append(tobe_port)

    def find_port(self, port_num_target):
        for port in self.total_port:
            if port.port_num == port_num_target:
                return port
        write_error("Port Number %d Not Found in Total Port Pool" % port_num_target)
        return None





























