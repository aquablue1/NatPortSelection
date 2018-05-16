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

class JobQueue(object):
    def __init__(self,file_path = "../data/sample1000.log"):
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
        self.finished_queue = []

        # Get start time and reset the ts for all records
        ts_start = min(float(job.ts) for job in self.total_job_queue)
        for job in self.total_job_queue:
            job.ts -= ts_start
        self.total_job_queue.sort(key=lambda x: x.ts, reverse=False)
        for job in self.total_job_queue:
            print(job)


if __name__ == '__main__':
    jq = JobQueue()