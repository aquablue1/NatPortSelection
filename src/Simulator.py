from src.JobQueue import TIME_GAP
from src.NAT import NAT
from src.LogInfo import write_perodicalInfo, set_logs_empty
SIMULATION_DURATION = 100
REPORT_INTERVAL = 60000

if __name__ == '__main__':
    file_path = "../data/sample1000.log"
    nat = NAT(file_path)
    time_left = SIMULATION_DURATION
    cur_time = 0
    # nat.port_pool
    # print(nat.queue.doing_queue)
    ready_list = []
    report_flag = REPORT_INTERVAL
    set_logs_empty(True)
    while time_left > 0:

        for job in ready_list:
            job_duration = job.duration
            chosen_port = nat.alg1_port_assign(job)
            nat.queue.set_doing(job)

        nat.port_pool.do_timepast(TIME_GAP)
        for port in nat.port_pool.pool_cooldown:
            if port.job.status == 2:
                nat.queue.doing_queue.remove(port.job)
                port.job.status = 3
                nat.queue.finish_queue.append(port.job)
        ready_list = nat.queue.get_ready(cur_time, TIME_GAP)

        time_left -= TIME_GAP
        cur_time += TIME_GAP
        report_flag -= 1
        if report_flag == 0:
            report_flag = REPORT_INTERVAL
            write_perodicalInfo("===== Current Time %f =======" % cur_time)
            write_perodicalInfo(" Current Pool INUSE %d" % len(nat.port_pool.pool_inuse))
            write_perodicalInfo(str(nat.port_pool.pool_inuse))
            write_perodicalInfo("----- Current Pool CoolDown %d -----" % len(nat.port_pool.pool_cooldown))
            write_perodicalInfo(str(nat.port_pool.pool_cooldown))
            write_perodicalInfo("----- Current Finished Job List %d -----" % len(nat.queue.finish_queue))
            write_perodicalInfo(str(nat.queue.finish_queue))
            write_perodicalInfo("=============================\n")
