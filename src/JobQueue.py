from src.LogInfo import write_error
import random


SIMULATION_DURATION = 1800
MAX_JOB_NUM = 10000
TIME_GAP = 0.01

class Job(object):
    def __init__(self, job_str):
        """
        Init a job object based on the job_string
        :param job_str: a string to describe the job
        """
        job_info_list = job_str.split("\t")
        self.job_str = job_str
        self.jobID = job_info_list[1]
        self.ts = float(job_info_list[0]) if float(job_info_list[0])>TIME_GAP else TIME_GAP
        self.origPort = int(job_info_list[3])
        self.endStatus = str(job_info_list[11])
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

    def increase_origPort(self, gap):
        """
        Reset the origPort
        :param gap: the gap between oldOrigPort and newOrigPort.
        :return:
        """
        self.origPort += gap
        if self.origPort >= 65535:
            self.origPort = self.origPort - 16383


class JobQueue(object):
    def __init__(self,file_path=None):
        """
        Job Queue Object, describe the overall jobs
        :param file_path: the folder where all job strings are stored.
        """
        if file_path is None:
            file_path = "../data/sample_test.log"
        self.total_job_queue = []
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if line.split("\t")[8] == "-":
                    # Get rid of those without a duration field.
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
        # self.add_rej_samples()

    def add_rej_samples(self):
        rej_mother = "1518627602.059990	CHQjGb3zKmXR8CNL01	136.159.160.4	64856	" \
                     "40.97.114.136	443	tcp	-	0.057991	0	0	REJ	T	F	" \
                     "0	Sr	1	64	1	40	(empty)"
        rejp1_num = 500
        for i in range(rejp1_num):
            ts = random.uniform(1, SIMULATION_DURATION)
            origPort = random.randint(49152, 65534)
            job = Job(rej_mother)
            job.ts = ts
            job.origPort = origPort
            job.endStatus = "REJPM1"
            self.insert_urgent_job(job)

        rejp2_num = 500
        for i in range(rejp2_num):
            ts = random.uniform(1, SIMULATION_DURATION)
            origPort = random.randint(49152, 65534)
            job = Job(rej_mother)
            job.ts = ts
            job.origPort = origPort
            job.endStatus = "REJPE2"
            self.insert_urgent_job(job)

        rejq_num = 1
        for i in range(rejq_num):
            ts = random.uniform(1, 10)
            origPort = random.randint(49152, 65534)
            job = Job(rej_mother)
            job.ts = ts
            job.origPort = origPort
            job.endStatus = "REJQ"
            self.insert_urgent_job(job)

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
            write_error("Error, current job %s not in QueueTodo." % job.jobID)
            return False

    def set_finish(self, job):
        if job in self.doing_queue:
            self.doing_queue.remove(job)
            self.finish_queue.append(job)
            return True
        else:
            write_error("Error, current job %s not in QueueDoing." % job.jobID)
            return False

    def insert_urgent_job(self, job):
        self.total_job_queue.append(job)
        self.todo_queue.append(job)

    def __str__(self):
        return [len(self.todo_queue), len(self.doing_queue),
                len(self.finish_queue)]


if __name__ == '__main__':
    jq = JobQueue()