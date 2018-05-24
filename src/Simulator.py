from src.JobQueue import TIME_GAP
from src.NAT import NAT
from src.LogInfo import write_perodicalInfo, set_logs_empty, write_runtimeInfo


SIMULATION_DURATION = 1800
# SIMULATION_DURATION = 500
REPORT_INTERVAL = 600


if __name__ == '__main__':
    file_path = "../data/sampleResid.log"
    nat = NAT(file_path)
    time_left = SIMULATION_DURATION
    cur_time = 0
    # nat.port_pool
    # print(nat.queue.doing_queue)
    ready_list = []
    report_flag = REPORT_INTERVAL
    outof_source_flag = False
    # clean all the dump files.
    set_logs_empty(True)
    print("Run A7 in campus real data.")
    print("Simulation Start, Total # of Job is %d." % len(nat.queue.total_job_queue))
    while time_left > 0:
        for job in ready_list:
            if len(nat.port_pool.pool_free)==0:
                write_runtimeInfo("Temporarily Run Outof Port At time %f for Job %s." % (cur_time, job.jobID))
                outof_source_flag = True
                break
            job_duration = job.duration
            chosen_port = nat.alg7_port_assign(job)
            nat.queue.set_doing(job)
            ready_list.remove(job)

        nat.port_pool.do_timepast(TIME_GAP)
        for port in nat.port_pool.pool_cooldown:
            if port.job.status == 2:
                port.job.status = 3
                nat.queue.set_finish(port.job)


        if outof_source_flag:
            outof_source_flag = False
            # print(ready_list)
            ready_list += nat.queue.get_ready(cur_time, TIME_GAP)
            ready_list = list(set(ready_list))
        else:
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
            write_perodicalInfo("----- Current Finished Job Num %d -----" % len(nat.queue.finish_queue))
            # write_perodicalInfo(str(nat.queue.finish_queue))
            write_perodicalInfo("=============================\n")
        if len(nat.queue.todo_queue)==0 and len(nat.queue.doing_queue)==0 and len(nat.port_pool.pool_cooldown)==0:
            # If all the jobs has been done, and all the port are set free, end the simulation.
            break

    print("Simulation Finish! Total Finished Job %d, Total Left Job %d" %(len(nat.queue.finish_queue),
                                                                          len(nat.queue.todo_queue)))