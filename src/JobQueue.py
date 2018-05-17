from src.LogInfo import write_error

MAX_JOB_NUM = 10000
TIME_GAP = 0.001

class Job(object):
    def __init__(self, job_str):
        job_info_list = job_str.split("\t")
        self.jobID = job_info_list[1]
        self.ts = float(job_info_list[0])
        self.origPort = int(job_info_list[3])

        # Initially the port num is not assigned
        self.realPort = -1

        self.fromPort = self.origPort
        self.toPort = int(job_info_list[5])
        self.status = 0
        # 0: to_do
        # 1: doing
        # 2: just_finished
        # 3: cleaned

        self.duration = float(job_info_list[8])

    def __str__(self):
        return "%s\t%f\t%d\t%d\t%d\t%d\t%f\n" % (self.jobID,
                                                 self.ts,
                                                 self.origPort,
                                                 self.realPort,
                                                 self.fromPort,
                                                 self.toPort,
                                                 self.duration
        )

    def __repr__(self):
        return "%s\t%f\t%d\t%d\t%d\t%d\t%f\n" % (self.jobID,
                                                 self.ts,
                                                 self.origPort,
                                                 self.realPort,
                                                 self.fromPort,
                                                 self.toPort,
                                                 self.duration
        )

class JobQueue(object):
    def __init__(self,file_path=None):
        if file_path is None:
            file_path = "../data/sample_test.log"
        self.total_job_queue = []
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if line.split("\t")[8] == "-":
                    continue
                job_tmp = Job(line)
                self.total_job_queue.append(job_tmp)

        self.todo_queue = []
        self.doing_queue = []
        self.finish_queue = []

        # Get start time and reset the ts for all records
        ts_start = min(float(job.ts) for job in self.total_job_queue)
        for job in self.total_job_queue:
            job.ts -= ts_start
        self.total_job_queue.sort(key=lambda x: x.ts, reverse=False)
        for job in self.total_job_queue:
            self.todo_queue.append(job)

    def get_ready(self, cur_time, time_gap):
        ready_list = []
        for job in self.todo_queue:
            if job.ts < (cur_time + time_gap):
                ready_list.append(job)

        return ready_list

    def set_doing(self, job):
        if job in self.todo_queue:
            self.todo_queue.remove(job)
            self.doing_queue.append(job)
            ### ?job.status = 1
            return True
        else:
            write_error("Error, current job %s not in QueueTodo" % job.jobID)
            return False

    def set_finish(self, job):
        if job in self.doing_queue:
            self.doing_queue.remove(job)
            self.finish_queue.append(job)
            return True
        else:
            write_error("Error, current job %s not in QueueDoing" % job.jobID)
            return False

    def __str__(self):
        return [len(self.todo_queue), len(self.doing_queue),
                len(self.finish_queue)]

if __name__ == '__main__':
    jq = JobQueue()